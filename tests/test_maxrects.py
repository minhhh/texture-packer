import unittest
from imagepacker import maxrect

class MaxRectsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def testCreatePixelRectSuccess(self):
        pr = maxrect.PixelRect(10, 10, 50, 60)
        self.assertEqual(pr.x, 10)
        self.assertEqual(pr.y, 10)
        self.assertEqual(pr.w, 50)
        self.assertEqual(pr.h, 60)

    def testCreateShortSideFit(self):
        mr = maxrect.MRHShortSideFit()
        self.assertEqual(mr.classname, "MRHShortSideFit")

    def testCreateMaxRect(self):
        mr = maxrect.MaxRects(128, 128)

    def testSplitFreeRects(self):
        mr = maxrect.MaxRects(128, 128)
        frmObj = maxrect.FrameObject(frame=maxrect.PixelRect(0, 0, 10, 10), sourceColorRect=maxrect.PixelRect(0, 0, 10, 10), sourceSize=[10, 10])

        self.assertTrue(mr.splitFreeRects(frmObj))
        # mr.printFreeRects()

    def testShortSideFit(self):
        mr = maxrect.MaxRects(128, 128, maxrect.MRHShortSideFit())
        frmObjs = [maxrect.FrameObject(sourceColorRect=maxrect.PixelRect(0, 0, 10, 10), sourceSize=[10, 10]),
                    maxrect.FrameObject(sourceColorRect=maxrect.PixelRect(0, 0, 12, 12), sourceSize=[12, 12]),
                    maxrect.FrameObject(sourceColorRect=maxrect.PixelRect(0, 0, 15, 15), sourceSize=[15, 15]),
                    maxrect.FrameObject(sourceColorRect=maxrect.PixelRect(0, 0, 20, 20), sourceSize=[20, 20]),
                    ]
        mr.insertFrmObjs(frmObjs)

        self.assertEqual(frmObjs[0].frame, maxrect.PixelRect(0, 0, 20, 20))
        self.assertEqual(frmObjs[1].frame, maxrect.PixelRect(0, 20, 15, 15))
        self.assertEqual(frmObjs[2].frame, maxrect.PixelRect(0, 35, 12, 12))
        self.assertEqual(frmObjs[3].frame, maxrect.PixelRect(0, 47, 10, 10))

    def testLongSideFit(self):
        mr = maxrect.MaxRects(128, 128, maxrect.MRHLongSideFit())
        frmObjs = [maxrect.FrameObject(sourceColorRect=maxrect.PixelRect(0, 0, 10, 10), sourceSize=[10, 10]),
                    maxrect.FrameObject(sourceColorRect=maxrect.PixelRect(0, 0, 12, 12), sourceSize=[12, 12]),
                    maxrect.FrameObject(sourceColorRect=maxrect.PixelRect(0, 0, 15, 15), sourceSize=[15, 15]),
                    maxrect.FrameObject(sourceColorRect=maxrect.PixelRect(0, 0, 20, 20), sourceSize=[20, 20]),
                    ]
        mr.insertFrmObjs(frmObjs)

        self.assertEqual(frmObjs[0].frame, maxrect.PixelRect(0, 0, 20, 20))
        self.assertEqual(frmObjs[1].frame, maxrect.PixelRect(0, 20, 15, 15))
        self.assertEqual(frmObjs[2].frame, maxrect.PixelRect(15, 20, 12, 12))
        self.assertEqual(frmObjs[3].frame, maxrect.PixelRect(20, 0, 10, 10))


    def testShortSideFit(self):
        mr = maxrect.MaxRects(128, 256, maxrect.MRHLongSideFit(), 1, 0)
        frmObjs = [
                    maxrect.FrameObject(sourceColorRect=maxrect.PixelRect(0, 0, 32, 32), sourceSize=[32, 32]),
                    maxrect.FrameObject(sourceColorRect=maxrect.PixelRect(0, 0, 32, 32), sourceSize=[32, 32]),
                    maxrect.FrameObject(sourceColorRect=maxrect.PixelRect(0, 0, 32, 32), sourceSize=[32, 32]),
                    maxrect.FrameObject(sourceColorRect=maxrect.PixelRect(0, 0, 32, 32), sourceSize=[32, 32]),
                    maxrect.FrameObject(sourceColorRect=maxrect.PixelRect(0, 0, 32, 32), sourceSize=[32, 32]),
                    maxrect.FrameObject(sourceColorRect=maxrect.PixelRect(0, 0, 32, 32), sourceSize=[32, 32]),
                    maxrect.FrameObject(sourceColorRect=maxrect.PixelRect(0, 0, 32, 32), sourceSize=[32, 32]),
                    maxrect.FrameObject(sourceColorRect=maxrect.PixelRect(0, 0, 32, 32), sourceSize=[32, 32]),
                    maxrect.FrameObject(sourceColorRect=maxrect.PixelRect(0, 0, 32, 32), sourceSize=[32, 32]),
                    maxrect.FrameObject(sourceColorRect=maxrect.PixelRect(0, 0, 32, 32), sourceSize=[32, 32]),
                    maxrect.FrameObject(sourceColorRect=maxrect.PixelRect(0, 0, 32, 32), sourceSize=[32, 32]),
                    ]
        mr.insertFrmObjs(frmObjs)

        self.assertEqual(frmObjs[0].frame, maxrect.PixelRect(0, 0, 32, 32))
        self.assertEqual(frmObjs[1].frame, maxrect.PixelRect(0, 33, 32, 32))
        self.assertEqual(frmObjs[9].frame, maxrect.PixelRect(33, 66, 32, 32))
        self.assertEqual(frmObjs[10].frame, maxrect.PixelRect(33, 99, 32, 32))



