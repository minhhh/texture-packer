PNGJ=`ls ../../lib | grep pngj`

jython -Dpython.path=../../lib/$PNGJ:../../src:../../libpython -c "import main; main.main()" "../imgs/arm0.png" "../imgs/arm1.png" --force-squared --max-size=64 --texture="out.png"

if [ -f out.png ]; then
    echo "Test case failed"
    exit 1
fi
