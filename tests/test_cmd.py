import os.path
import unittest
import java.io
import imagepacker.cmd as cmd
import imagepacker.maxrect as maxrect

class PngjTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def testBorderPadding(self):
        allow_rotation = False
        heuristics = maxrect.MRHeuristicsType.RECTBESTSHORTSIDEFIT
        width, height = 128, 128
        filelist = cmd.read_file_list(["macrotests/imgs/arm0.png", "macrotests/imgs/arm1.png"])
        frmObjs = cmd.read_image_info(filelist)
        canFit = cmd.try_fit(frmObjs, width, height, heuristics, allow_rotation, 0, 1)

        self.assertEqual(frmObjs[0].frame, maxrect.PixelRect(1, 1, 52, 91))
        self.assertEqual(frmObjs[1].frame, maxrect.PixelRect(53, 1, 52, 91))

    def testShapePadding(self):
        allow_rotation = False
        heuristics = maxrect.MRHeuristicsType.RECTBESTSHORTSIDEFIT
        width, height = 128, 128
        filelist = cmd.read_file_list(["macrotests/imgs/arm0.png", "macrotests/imgs/arm1.png"])
        frmObjs = cmd.read_image_info(filelist)
        canFit = cmd.try_fit(frmObjs, width, height, heuristics, allow_rotation, 2, 1)

        self.assertEqual(frmObjs[0].frame, maxrect.PixelRect(1, 1, 52, 91))
        self.assertEqual(frmObjs[1].frame, maxrect.PixelRect(55, 1, 52, 91))

    def testRotate(self):
        allow_rotation = True
        heuristics = maxrect.MRHeuristicsType.RECTBESTSHORTSIDEFIT
        width, height = 256, 64
        filelist = cmd.read_file_list(["macrotests/imgs/arm0.png", "macrotests/imgs/arm1.png"])
        frmObjs = cmd.read_image_info(filelist)
        canFit = cmd.try_fit(frmObjs, width, height, heuristics, allow_rotation, 2, 1)

        self.assertEqual(frmObjs[0].frame, maxrect.PixelRect(1, 1, 52, 91))
        self.assertEqual(frmObjs[1].frame, maxrect.PixelRect(94, 1, 52, 91))


    def testScaleSize(self):
        failed, width, height = cmd.scale_size(16, 16, None, None, 128, 128, None, None)
        self.assertFalse(failed)
        self.assertEqual(width, 16)
        self.assertEqual(height, 32)

        failed, width, height = cmd.scale_size(16, 32, None, None, 128, 128, None, None)
        self.assertFalse(failed)
        self.assertEqual(width, 32)
        self.assertEqual(height, 32)

        failed, width, height = cmd.scale_size(16, 128, None, None, 128, 128, None, None)
        self.assertFalse(failed)
        self.assertEqual(width, 32)
        self.assertEqual(height, 128)

        failed, width, height = cmd.scale_size(128, 128, None, None, 128, 128, None, None)
        self.assertTrue(failed)

        failed, width, height = cmd.scale_size(128, 128, 128, 128, None, None, None, None)
        self.assertTrue(failed)

        failed, width, height = cmd.scale_size(16, 16, None, None, None, None, None, 64)
        self.assertFalse(failed)
        self.assertEqual(width, 32)
        self.assertEqual(height, 32)

        failed, width, height = cmd.scale_size(64, 64, None, None, None, None, None, 64)
        self.assertTrue(failed)

