PNGJ=`ls ../../lib | grep pngj`

jython -Dpython.path=../../lib/$PNGJ:../../src:../../libpython -c "import main; main.main()" "../imgs" --max-width=1024 --max-height=1024 --shape-padding=1 --border-padding=0 --texture="out.png" --data="out.plist" --maxrects-heuristics="areafit"

if [ ! -f out.png ]; then
    echo "Test case failed"
    exit 1
fi
