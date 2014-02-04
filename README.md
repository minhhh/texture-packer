texture-packer
==============

A jython command line implementation of the popular TexturePacker.

### Examples
Show help

    java -jar out/TexturePacker.jar -h

Pack files and/or folders of images

    java -jar out/TexturePacker.jar "macrotests/imgs/arm0.png" "macrotests/imgs/arm1.png" --force-squared --max-size=1024 --shape-padding=2 --border-padding=1 --sheet="out.png" --data="out.plist"
