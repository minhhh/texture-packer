"""
Usage: ImagePacker [--texture=TEXTURE] [--data=DATA] [--format=FORMAT]
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
  -h --help                         Show this help message and exit
  --version                         Print version information
  -t TEXTURE --texture=TEXTURE      Name of the output texture, supported formats:
                                       png     - 32bit, allows all pixel formats
                                       [default: out.png]
  -d DATA --data=DATA               Name of the data file to write [default: out.plist]
  -f FORMAT --format=FORMAT         Format to write [default: cocos2d]
                                    Available formats:
                                        cocos2d             plist format for cocos2d
  -a ALG --algorithm=ALG            Choose algorithm
                                         MaxRects        Powerful packing algorithm (extended)
  --maxrects-heuristics=HEURISTICS  Heuristics [default: best]
                                        best              Detects best option
                                        shortsidefit      Short side fit
                                        longsidefit       Long side fit
                                        bottomleft        Bottom left
                                        contactpoint      Contact point
                                        areafit           Area fit

Rotation Options:
  --rotation                        Allow rotation
  --no-rotation                     Not allow rotation

Auto Alias Options:
  --enable-alias                    Enable auto alias mode.
  --disable-alias                   Disable auto alias mode.

Decrease Color Options:
  --decreasecolor                   Decrease color
  --no-decreasecolor                No decrease color

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
"""

# https://github.com/suning/packsprite/blob/master/maxrects.py
# https://github.com/juj/RectangleBinPack/blob/master/MaxRectsBinPack.cpp
# http://clb.demon.fi/files/RectangleBinPack.pdf

import sys, os
from docopt import docopt
from imagepacker import utils

def main():
    try:
        arguments = docopt(__doc__, version='TexturePacker 0.1')
        print "Starting ..."
        import imagepacker.cmd
        imagepacker.cmd.launch(arguments)
    except Exception:
        utils.print_last_exception()
        pass
    except SystemExit as e:
        print e
        pass
