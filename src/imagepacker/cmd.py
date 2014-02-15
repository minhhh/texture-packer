import os, sys
from os import walk
import maxrect
from ar.com.hjg.pngj import PngReader, PngWriter, ImageLineHelper, ImageInfo, ImageLineInt
from ar.com.hjg.pngj.chunks import PngChunkPLTE, ChunksList, PngChunkIHDR, PngChunkTRNS
import java
from java.nio import ByteBuffer

def readFileList(fl):
    result = []
    for filename in fl:
        if os.path.isfile(filename):
            result.append(filename)
        elif os.path.isdir(filename):
            result += readDirImgs(filename)
    return result

def readDirImgs(dir):
    result = []
    for (dirpath, dirnames, filenames) in walk(dir):
        for filename in [f for f in filenames if os.path.splitext(f)[1] == '.png']:
            result.append(dirpath + os.path.sep + filename)
    return result

def readImageInfo(filelist):
    result = []
    pr = None
    for file in filelist:
        try:
            pr = PngReader(java.io.File(file))
            result.append(maxrect.FrameObject(name=file, sourceColorRect=maxrect.PixelRect(0, 0, pr.imgInfo.cols, pr.imgInfo.rows), sourceSize=[pr.imgInfo.cols, pr.imgInfo.rows]))
        finally:
            if pr:
                pr.close()

    return result

def tryFit(frmObjs, width, height, heuristics, allow_rotation, shape_padding, border_padding):
    heuristicsCls = maxrect.MRHeuristicsType.get(heuristics)

    mr = maxrect.MaxRects(width, height, heuristicsCls(allow_rotation, shape_padding, border_padding), shape_padding, border_padding)
    return mr.insertFrmObjs(frmObjs)

TWO_MAXINT = 2 * sys.maxint + 2
def getFileData(frmObjs):
    result = []
    for frmObj in frmObjs:
        pr = None
        try:
            pr = PngReader(java.io.File(frmObj.name))
            imgData = []
            pal, trns = None, None
            if pr.imgInfo.indexed:
                pal = pr.getMetadata().getPLTE()
                trns = pr.getChunksList().getById(PngChunkTRNS.ID)
                trns = trns[0] if len(trns) else None
            for i in range(pr.imgInfo.rows):
                imgLine = pr.readRow(i)
                buf = []
                line_buf = []
                if pr.imgInfo.indexed:
                    line_buf = ImageLineHelper.palette2rgba(imgLine, pal, trns, None)
                    if trns:
                        for j in range(pr.imgInfo.cols):
                            offset = j * 4
                            pixel = ((line_buf[offset + 3] & 0xff) << 24) | ((line_buf[offset] & 0xff) << 16) | ((line_buf[offset + 1] & 0xff) << 8) | ((line_buf[offset + 2] & 0xff))
                            if pixel > sys.maxint:
                                pixel = pixel - TWO_MAXINT
                            buf.append(pixel)
                    else:
                        for j in range(pr.imgInfo.cols):
                            offset = j * 3
                            pixel = (-1 << 24) | ((line_buf[offset] & 0xff) << 16) | ((line_buf[offset + 1] & 0xff) << 8) | ((line_buf[offset + 2] & 0xff))
                            if pixel > sys.maxint:
                                pixel = pixel - TWO_MAXINT
                            buf.append(pixel)
                else:
                    for j in range(pr.imgInfo.cols):
                        if pr.imgInfo.alpha:
                            buf.append(ImageLineHelper.getPixelARGB8(imgLine, j))
                        else:
                            buf.append((-1 << 24) | ImageLineHelper.getPixelRGB8(imgLine, j))

                imgData.append(buf)
            result.append({"data": imgData, "frmObj": frmObj})
        finally:
            if pr:
                pr.close()
    return result

def getPixelRGBA(imgData, row, col):
    for data in imgData:
        if data["frmObj"].rotated:
            if col >= data["frmObj"].frame.x \
            and col < data["frmObj"].frame.x + data["frmObj"].frame.h \
            and row >= data["frmObj"].frame.y \
            and row < data["frmObj"].frame.y + data["frmObj"].frame.w:
                return data["data"][data["frmObj"].frame.h - 1 - col + data["frmObj"].frame.x + data["frmObj"].offset[1]][row - data["frmObj"].frame.y + data["frmObj"].offset[0]]
        else:
            if col >= data["frmObj"].frame.x \
            and col < data["frmObj"].frame.x + data["frmObj"].frame.w \
            and row >= data["frmObj"].frame.y \
            and row < data["frmObj"].frame.y + data["frmObj"].frame.h:
                return data["data"][row - data["frmObj"].frame.y + data["frmObj"].offset[1]][col - data["frmObj"].frame.x + data["frmObj"].offset[0]]
    return 0

def packImages(imageDataList, width, height, args):
    result = True
    oFile = java.io.File(args['--texture'])
    wr = None
    try:
        imi = ImageInfo(width, height, 8, True)
        wr = PngWriter(oFile, imi, True)
        for i in range(height):
            imgLine = ImageLineInt(imi)
            for j in range(width):
                pixel = getPixelRGBA(imageDataList, i, j)
                ImageLineHelper.setPixelRGBA8(imgLine, j, pixel)
            wr.writeRow(imgLine)
        wr.end()
    except Exception as e:
        print "Exception ", e
        result = False
    finally:
        if wr:
            wr.close()
    return result

def processImages(frmObjs, args):
    allow_rotation = not args['--no-rotation']
    heuristics = MR_HEURISTICS[args["--maxrects-heuristics"]]

    fixed_width =  int(args['--width']) if args['--width'] else None
    fixed_height =  int(args['--height']) if args['--height'] else None
    max_width =  int(args['--max-width']) if args['--max-width'] else None
    max_height =  int(args['--max-height']) if args['--max-height'] else None
    forced_squared = args['--force-squared']
    fixed_size =  int(args['--size']) if args['--size'] else None
    max_size =  int(args['--max-size']) if args['--max-size'] else None
    shape_padding = int(args['--shape-padding']) if args['--shape-padding'] else None
    border_padding = int(args['--border-padding']) if args['--border-padding'] else None

    if fixed_width:
        width = fixed_width
    else:
        width = 16
    if fixed_height:
        height = fixed_height
    else:
        height = 16
    if fixed_size:
        width = height = fixed_size

    total_area, canFit, failed = cal_total_area(frmObjs), False, False
    while not canFit and not failed:
        if width * height < total_area:
            canFit = False
        else:
            canFit = tryFit(frmObjs, width, height, heuristics, allow_rotation, shape_padding, border_padding)
        if not canFit:
            failed, width, height = scale_size(width, height, fixed_width, fixed_height, max_width, max_height, fixed_size, max_size)

    return canFit, width, height

def cal_total_area(frmObjs):
    result = 0
    for frmObj in frmObjs:
        result += frmObj.sourceColorRect.w * frmObj.sourceColorRect.h

    return result

def scale_size(width, height, fixed_width, fixed_height, max_width, max_height, size, max_size):
    failed_scale = True
    new_height = height
    new_width = width

    def scale_width():
        if max_width and width < max_width and width * 2 <= max_width and failed_scale:
            return width * 2, False
        return width, failed_scale

    def scale_height():
        if max_height and height < max_height and height * 2 <= max_height and failed_scale:
            return height * 2, False
        return height, failed_scale

    if width < height:
        new_width, failed_scale = scale_width()
        new_height, failed_scale = scale_height()
    else:
        new_height, failed_scale = scale_height()
        new_width, failed_scale = scale_width()

    if max_size and width < max_size and width * 2 <= max_size and failed_scale:
        new_width = new_height = width * 2
        failed_scale = False

    return failed_scale, new_width, new_height

def packData(frmObjs, width, height, args):
    fp = None
    header = """
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
    <dict>
        <key>frames</key>
        <dict>"""
    tail = """
        </dict>
        <key>metadata</key>
        <dict>
            <key>format</key>
            <integer>2</integer>
            <key>size</key>
            <string>{%d,%d}</string>
        </dict>
    </dict>
</plist>""" % (width, height)
    oFn = args['--data']
    try:
        fp = open(oFn, 'w')
        fp.write(header)
        for frm in frmObjs:
            fp.write(maxrect.DataExporter.exportToJson(frm))
        fp.write(tail)
    finally:
        if fp:
            fp.close()


MR_HEURISTICS = {
    "shortsidefit":0,
    "longsidefit":1,
    "bottomleft":2,
    "contactpoint":3,
    "areafit":4,
    "best":5
}

def launch(args):
    # print args
    filelist = readFileList(args['FILE'])
    frmObjs = readImageInfo(filelist)

    canFit, width, height = processImages(frmObjs, args)
    if canFit:
        packImages(getFileData(frmObjs), width, height, args)
        packData(frmObjs, width, height, args)
    else:
        print "Cannot pack images!"

    # for fileinfo in frmObjs:
    #     print fileinfo

