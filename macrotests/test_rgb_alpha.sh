PNGJ=`ls ../../lib | grep pngj`

jython -Dpython.path=../../lib/$PNGJ:../../src:../../libpython -c "import main; main.main()" -v  "../imgs/cover1.png" "../imgs/cover2.png" --force-squared --max-size=128 --texture="out.png" --data="out.plist"

if [ ! -f out.png ]; then
    echo "Test case failed"
    exit 1
fi
