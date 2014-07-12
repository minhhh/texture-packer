import os.path
import unittest
import java.io
from ar.com.hjg.pngj import *

class PngjTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def testReadPng(self):
        try:
            reader = PngReader(java.io.File("macrotests/imgs/arm0.png"))
            length = reader.imgInfo.cols * reader.imgInfo.bitspPixel
            buf = []
            for i in range(reader.imgInfo.rows):
                imgLine = reader.readRow(i)
                scanLine = imgLine.getScanline()
                # print imgLine.getSize(), reader.imgInfo.channels, imgLine.getElem(1)
                # print scanLine
                # print imgLine.getElem(26)getPixelARGB8
                # print ImageLineHelper.getPixelARGB8(imgLine, 26)


        finally:
            if reader:
                reader.close()


    def testCreatePng(self):
        oFile = java.io.File("out.png")
        wr = None
        try:
            imi = ImageInfo(128, 128, 8, True)
            wr = PngWriter(oFile, imi, True)
        except Exception:
            pass
        finally:
            if wr:
                wr.close()

