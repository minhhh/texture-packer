texture-packer
==============

A jython command line implementation of the popular TexturePacker.

### Features
  * Formats: Currently only support `plist`
  * Rotation: Enable by default. Add `--no-rotation` to force no rotation

### Parameters

    Usage: ImagePacker [--sheet=SHEET] [--data=DATA] [--format=FORMAT]
                    [--algorithm=ALG [--maxrects-heuristics=HEURISTIC]]
                    [--rotation | --no-rotation]
                    ( ((--width=WIDTH | --max-width=MAXWIDTH) (--height=HEIGHT | --max-height=MAXHEIGHT)) | (--force-squared (--max-size=MAXSIZE | --size=SIZE)) )
                    [--enable-alias | --disable-alias] [--decreasecolor | --no-decreasecolor]
                    [--shape-padding=SHAPEPADDING] [--border-padding=BORDERPADDING]
                    [--trim | --no-trim]
                    [--opt=OPT]
                    FILE...
        ImagePacker --version

    Process FILE and pack them into a texture sheet and texture data.

    Arguments:
    FILE        FILE can be multiple image files (currently only support .png)
                or directories.

    General Options:
    -h --help                   Show this help message and exit
    --version                   Print version information
    -s SHEET --sheet=SHEET      Name of the sheet to write, supported formats:
                                    png     - 32bit, allows all pixel formats
                                [default: out.png]
    -d DATA --data=DATA         Name of the data file to write [default: out.plist]
    -f FORMAT --format=FORMAT   Format to write [default: cocos2d]
                                Available formats:
                                    cocos2d             plist format for cocos2d
    -a ALG --algorithm=ALG      Choose algorithm
                                    MaxRects        Powerful packing algorithm (extended)
    --maxrects-heuristics=HEURISTICS  Heuristics [default: best]
                                            best              Detects best option
                                            shortsidefit      Short side fit
                                            longsidefit       Long side fit
                                            bottomleft        Bottom left
                                            contactpoint      Contact point
                                            areafit           Area fit

    Rotation Options:
    --rotation                  Allow rotation. Enable by default.
    --no-rotation               Not allow rotation

    Auto Alias Options:
    --enable-alias			  Enable auto alias mode.
    --disable-alias			  Disable auto alias mode.

    Decrease Color Options:
    --decreasecolor             Decrease color
    --no-decreasecolor          No decrease color

    Dimensions Options:
    --width=WIDTH                   Sets fixed width for texture
    --height=HEIGHT                 Sets fixed height for texture
    --max-width=WIDTH               Sets max width for autowidth
    --max-height=HEIGHT             Sets max height for autoheight
    --force-squared                 Force squared dimension
    --size=SIZE                     Set fixed size when force-squared
    --max-size=MAXSIZE              Set max size when force-squared

    Padding Options:
    --shape-padding=SHAPEPADDING    Sets a padding around each shape, value is in pixels [default: 2]
    --border-padding=BORDERPADDING  Sets a padding around each shape, and to the border, value is in pixels [default: 0]
    --trim                          Removes transparent parts of the sprites and stores them with
                                    original size. On by default.
    --no-trim                       Do not trim the images

    Graphics optimization (extended only) Options:
    --opt=OPT     Optimized output for given pixel formats. Supported formats are:
                        RGBA8888

### Examples
Show help

    java -jar out/TexturePacker.jar -h

Pack files and/or folders of images

    java -jar out/TexturePacker.jar "macrotests/imgs/arm0.png" "macrotests/imgs/arm1.png"
    --force-squared --max-size=1024 --shape-padding=2 --border-padding=1 --sheet="out.png" --data="out.plist"


### RELEASE NOTES

Version 0.1
  * Add cocos2d format
  * Add 2 maxrect heuristics: BestShortSideFit, BestLongSideFit

Todo
  * Add maxrect heuristics: BestAreaFit, BottomLeft, BestContactPoint, Best
