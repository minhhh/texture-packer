PNGJ=`ls ../../lib | grep pngj`

jython -Dpython.path=../../lib/$PNGJ:../../src:../../libpython -c "import main; main.main()" "../imgs" --max-width=128 --max-height=256 --shape-padding=1 --border-padding=0 --texture="out.png" --data="out.plist"

if [ ! -f out.png ]; then
    echo "Test case failed"
    exit 1
fi
