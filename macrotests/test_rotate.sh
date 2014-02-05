PNGJ=`ls ../../lib | grep pngj`

jython -Dpython.path=../../lib/$PNGJ:../../src:../../libpython -c "import main; main.main()" "../imgs/arm0.png" "../imgs/arm1.png" --max-width=256 --max-height=64 --shape-padding=2 --border-padding=1 --texture="out.png" --data="out.plist"

if [ ! -f out.png ]; then
    echo "Test case failed"
    exit 1
fi
