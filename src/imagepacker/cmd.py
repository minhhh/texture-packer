import os, sys
from os import walk
import maxrect
from ar.com.hjg.pngj import PngReader, PngWriter, ImageLineHelper, ImageInfo, ImageLineInt
from ar.com.hjg.pngj.chunks import PngChunkPLTE, ChunksList, PngChunkIHDR, PngChunkTRNS
import java
from java.nio import ByteBuffer
import codecs

ARGS = {}
MR_HEURISTICS = {
    "shortsidefit": maxrect.MRHeuristicsType.RECTBESTSHORTSIDEFIT,
    "longsidefit": maxrect.MRHeuristicsType.RECTBESTLONGSIDEFIT,
    "bottomleft": maxrect.MRHeuristicsType.RECTBOTTOMLEFT,
    "contactpoint": maxrect.MRHeuristicsType.RECTBESTAREAFIT,
    "areafit": maxrect.MRHeuristicsType.RECTBESTAREAFIT,
    "best": maxrect.MRHeuristicsType.RECTBESTFIT
}


def read_file_list(fl):
    result = []
    for filename in fl:
        if os.path.isfile(filename):
            result.append(filename)
        elif os.path.isdir(filename):
            result += read_dir_imgs(filename)
    return result

def read_dir_imgs(dir):
    result = []
    for (dirpath, dirnames, filenames) in walk(dir):
        for filename in [f for f in filenames if os.path.splitext(f)[1] == '.png']:
            result.append(dirpath + os.path.sep + filename)
    return result

def read_image_info(filelist):
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

def try_fit(frm_objs, width, height, heuristics, allow_rotation, shape_padding, border_padding):
    if heuristics == maxrect.MRHeuristicsType.RECTBESTFIT:
        for i in range(maxrect.MRHeuristicsType.RECTBESTFIT):
            heuristicsCls = maxrect.MRHeuristicsType.get(i)
            mr = maxrect.MaxRects(width, height, heuristicsCls(allow_rotation, shape_padding, border_padding), shape_padding, border_padding)
            if mr.insert_frm_objs(frm_objs):
                return True
        return False
    else:
        heuristicsCls = maxrect.MRHeuristicsType.get(heuristics)
        mr = maxrect.MaxRects(width, height, heuristicsCls(allow_rotation, shape_padding, border_padding), shape_padding, border_padding)
        return mr.insert_frm_objs(frm_objs)

TWO_MAXINT = 2 * sys.maxint + 2
def get_file_data(frm_objs):
    result = []
    for frmObj in frm_objs:
        pr = None
        try:
            if ARGS['--verbose']:
                print "Processing ", frmObj.name
            pr = PngReader(java.io.File(frmObj.name))
            imgData = []
            pal, trns = None, None
            pal = pr.getMetadata().getPLTE()
            trns = pr.getMetadata().getTRNS()

            for i in range(pr.imgInfo.rows):
                imgLine = pr.readRow(i)
                ImageLineHelper.scaleUp(imgLine)
                buf = []
                line_buf = []
                if pr.imgInfo.indexed: # INDEXED PNG
                    line_buf = ImageLineHelper.palette2rgba(imgLine, pal, trns, None)
                    if trns:
                        for j in range(pr.imgInfo.cols):
                            offset = j * 4
                            pixel = ((line_buf[offset + 3] & 0xff) << 24) | ((line_buf[offset] & 0xff) << 16) | ((line_buf[offset + 1] & 0xff) << 8) | ((line_buf[offset + 2] & 0xff))
                            if pixel > sys.maxint:
                                pixel -= TWO_MAXINT
                            buf.append(pixel)
                    else:
                        for j in range(pr.imgInfo.cols):
                            offset = j * 3
                            pixel = (-1 << 24) | ((line_buf[offset] & 0xff) << 16) | ((line_buf[offset + 1] & 0xff) << 8) | ((line_buf[offset + 2] & 0xff))
                            if pixel > sys.maxint:
                                pixel -= TWO_MAXINT
                            buf.append(pixel)
                else: # RGB PNG
                    for j in range(pr.imgInfo.cols):
                        if ARGS['--verbose']:
                            print j, pr.imgInfo, pr.imgInfo.cols

                        if pr.imgInfo.greyscale:
                            ga = trns.getGray() if trns else -1
                            line_buf = imgLine.scanline
                            offset = j * 2 if pr.imgInfo.alpha else j
                            g = line_buf[offset]
                            alpha = (line_buf[offset + 1] & 0xFF) if pr.imgInfo.alpha else (255 if g != ga else 0)
                            pixel = (alpha << 24) | ((g & 0xff) << 16) | ((g & 0xff) << 8) | ((g & 0xff))
                            if pixel > sys.maxint:
                                pixel -= TWO_MAXINT
                            buf.append(pixel)
                        else:
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

def get_pixel_RGBA(imgData, row, col):
    for data in imgData:
        if data["frmObj"].rotated:
            if data["frmObj"].frame.x <= col < data["frmObj"].frame.x + data["frmObj"].frame.h \
                    and data["frmObj"].frame.y <= row < data["frmObj"].frame.y + data["frmObj"].frame.w:
                return data["data"][data["frmObj"].frame.h - 1 - col + data["frmObj"].frame.x + data["frmObj"].offset[1]][row - data["frmObj"].frame.y + data["frmObj"].offset[0]]
        else:
            if data["frmObj"].frame.x <= col < data["frmObj"].frame.x + data["frmObj"].frame.w \
                    and row >= data["frmObj"].frame.y \
            and row < data["frmObj"].frame.y + data["frmObj"].frame.h:
                return data["data"][row - data["frmObj"].frame.y + data["frmObj"].offset[1]][col - data["frmObj"].frame.x + data["frmObj"].offset[0]]
    return 0

def pack_images(imageDataList, width, height, args):
    result = True
    oFile = java.io.File(args['--texture'])
    wr = None
    try:
        imi = ImageInfo(width, height, 8, True)
        wr = PngWriter(oFile, imi, True)
        for i in range(height):
            imgLine = ImageLineInt(imi)
            for j in range(width):
                pixel = get_pixel_RGBA(imageDataList, i, j)
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

def process_images(frm_objs, args):
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

    total_area, can_fit, failed = cal_total_area(frm_objs), False, False
    while not can_fit and not failed:
        if width * height < total_area:
            can_fit = False
        else:
            can_fit = try_fit(frm_objs, width, height, heuristics, allow_rotation, shape_padding, border_padding)
        if not can_fit:
            failed, width, height = scale_size(width, height, fixed_width, fixed_height, max_width, max_height, fixed_size, max_size)

    return can_fit, width, height

def cal_total_area(frm_objs):
    result = 0
    for frmObj in frm_objs:
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

def pack_data(frm_objs, width, height, output_file):
    file_ext = os.path.splitext(output_file)
    if file_ext[1] == '.plist':
        pack_data_plist(frm_objs, width, height, output_file)

def pack_data_plist(frm_objs, width, height, output_file):
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
    oFn = output_file
    with codecs.open(oFn, 'w', encoding='utf-8') as fh:
        fh.write(header)
        for frm in frm_objs:
            fh.write(maxrect.DataExporter.export_to_json(frm))
        fh.write(tail)

def launch(args):
    global ARGS
    ARGS = args
    filelist = read_file_list(args['FILE'])
    frm_objs = read_image_info(filelist)

    can_fit, width, height = process_images(frm_objs, args)
    if can_fit:
        pack_images(get_file_data(frm_objs), width, height, args)
        pack_data(frm_objs, width, height, args['--data'])
    else:
        print "Cannot pack images!"

    # for fileinfo in frm_objs:
    #     print fileinfo

