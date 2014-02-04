import os, sys, copy

def overrides(interface_class):
    def overrider(method):
        assert(method.__name__ in dir(interface_class))
        return method
    return overrider

class PixelRect(object):
    'class for rectangle: x, y, w, h'
    def __init__(self, x=0, y=0, w=0, h=0):
        for n, v in locals().iteritems():
            if n != 'self':
                setattr(self, n, v)

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "x:%s y:%s w:%s h:%s" % (self.x, self.y, self.w, self.h)

class MRHeuristicsType(object):
    RECTBESTSHORTSIDEFIT = 0
    RECTBOTTOMLEFTRULE   = 1
    RECTCONTACTPOINTRULE = 2
    RECTBESTLONGSIDEFIT  = 3
    RECTBESTAREAFIT      = 4
    RECTBESTAREAFIT      = 5

    @staticmethod
    def get(i):
        return (MRHShortSideFit, MRHLongSideFit, MRHLongSideFit, MRHLongSideFit, MRHLongSideFit, MRHLongSideFit)[i]

MAX              = sys.maxsize

class MRHeuristics(object):
    def __init__(self, allow_rotation=False, shape_padding=0, border_padding=0):
        self._allow_rotation = allow_rotation
        self._shape_padding = shape_padding
        self._border_padding = border_padding

    @property
    def classname(self):
        return self.__class__.__name__

    def placeFrame(self, w, h, freeRects, rw, rh):
        return None, None

class MRHLongSideFit(MRHeuristics):

    @overrides(MRHeuristics)
    def placeFrame(self, w, h, freeRects, rw, rh):
        rotated = False
        result = PixelRect()
        bestShortSide = bestLongSide = MAX
        for r in freeRects:
            if r.w >= rw and r.h >= rh:
                gapw = r.w - rw
                gaph = r.h - rh
                shortSide = min(gapw, gaph)
                longSide = max(gapw, gaph)
                if (bestLongSide > longSide or
                    (bestLongSide == longSide and
                     bestShortSide > shortSide)):
                        rotated = False
                        bestShortSide = shortSide
                        bestLongSide = longSide
                        result = PixelRect(r.x, r.y, rw, rh)
            if self._allow_rotation and r.w >= rh and r.h >= rw:
                gapw = r.w - rh
                gaph = r.h - rw
                shortSide = min(gapw, gaph)
                longSide = max(gapw, gaph)
                if (bestLongSide > longSide or
                    (bestLongSide == longSide and
                     bestShortSide > shortSide)):
                        rotated = True
                        bestShortSide = shortSide
                        bestLongSide = longSide
                        result = PixelRect(r.x, r.y, rw, rh)
        if bestShortSide == MAX:
            return None, None
        return result, rotated

class MRHShortSideFit(MRHeuristics):
    @overrides(MRHeuristics)
    def placeFrame(self, w, h, freeRects, rw, rh):
        rotated = False
        result = PixelRect()
        bestShortSide = bestLongSide = MAX
        for r in freeRects:
            if r.w >= rw and r.h >= rh:
                gapw = r.w - rw
                gaph = r.h - rh
                shortSide = min(gapw, gaph)
                longSide = max(gapw, gaph)
                if (bestShortSide > shortSide or
                    (bestShortSide == shortSide and
                     bestLongSide > longSide)):
                        rotated = False
                        bestShortSide = shortSide
                        bestLongSide = longSide
                        result = PixelRect(r.x, r.y, rw, rh)
            if self._allow_rotation and r.w >= rh and r.h >= rw:
                gapw = r.w - rh
                gaph = r.h - rw
                shortSide = min(gapw, gaph)
                longSide = max(gapw, gaph)
                if (bestShortSide > shortSide or
                    (bestShortSide == shortSide and
                     bestLongSide > longSide)):
                        rotated = True
                        bestShortSide = shortSide
                        bestLongSide = longSide
                        result = PixelRect(r.x, r.y, rw, rh)
        if bestShortSide == MAX:
            return None, None
        return result, rotated

class FrameObject(object):
    'frameObject contains: frame, rotated, offset, sourceColorRect, sourceSize'
    def __init__(self, name='frame.png', frame=PixelRect(), rotated=False, offset=[0, 0],
                 sourceColorRect=PixelRect(), sourceSize=[0, 0]):
        for n, v in locals().iteritems():
            if n != 'self':
                setattr(self, n, v)

    def __str__(self):
        return '''
            <key>%s</key>
            <dict>
                <key>frame</key>
                <string>{{%d, %d}, {%d, %d}}</string>
                <key>offset</key>
                <string>{%d, %d}</string>
                <key>rotated</key>
                <%s/>
                <key>sourceColorRect</key>
                <string>{{%d, %d}, {%d, %d}}</string>
                <key>sourceSize</key>
                <string>{%d, %d}</string>
            </dict>''' % (self.name, self.frame.x, self.frame.y, self.frame.w, self.frame.h,
                          self.offset[0], self.offset[1], 'true' if self.rotated else 'false',
                          self.sourceColorRect.x, self.sourceColorRect.y,
                          self.sourceColorRect.w, self.sourceColorRect.h,
                          self.sourceSize[0], self.sourceSize[1])

class DataExporter(object):
    @staticmethod
    def exportToJson(frmObj):
        return '''
            <key>%s</key>
            <dict>
                <key>frame</key>
                <string>{{%d, %d}, {%d, %d}}</string>
                <key>offset</key>
                <string>{%d, %d}</string>
                <key>rotated</key>
                <%s/>
                <key>sourceColorRect</key>
                <string>{{%d, %d}, {%d, %d}}</string>
                <key>sourceSize</key>
                <string>{%d, %d}</string>
            </dict>''' % (os.path.basename(frmObj.name), frmObj.frame.x, frmObj.frame.y, frmObj.frame.w, frmObj.frame.h,
                          frmObj.offset[0], frmObj.offset[1], 'true' if frmObj.rotated else 'false',
                          frmObj.sourceColorRect.x, frmObj.sourceColorRect.y,
                          frmObj.sourceColorRect.w, frmObj.sourceColorRect.h,
                          frmObj.sourceSize[0], frmObj.sourceSize[1])


class MaxRects(object):
    """
    Maximum rectangles algorithm.
    Supported heuristics:

    """

    def __init__(self, w, h, heuristics = None, shape_padding=0, border_padding=0):
        self._width = w - 2 * border_padding
        self._height = h - 2 * border_padding
        self._shape_padding = shape_padding
        self._border_padding = border_padding
        self._freeRects = [PixelRect(0, 0, self._width, self._height)]
        if heuristics == None:
            heuristics = MRHShortSideFit()
        self._heuristics = heuristics

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def freeRects(self):
        return self._freeRects

    def printFreeRects(self):
        for rect in self._freeRects:
            print rect

    @property
    def heuristics(self):
        return self._heuristics

    def insertFrmObjs(self, frmObjs):
        frmObjs.sort(key=lambda f: f.sourceColorRect.w * f.sourceColorRect.h, reverse=True)
        for frmObj in frmObjs:
            newFrame, rotated = self.heuristics.placeFrame(self.width, self.height, self.freeRects, frmObj.sourceColorRect.w + self._shape_padding, frmObj.sourceColorRect.h + self._shape_padding)
            if newFrame:
                frmObj.frame = newFrame
                frmObj.rotated = rotated
                self.splitFreeRects(frmObj)
            else:
                return False

        # insert border offsets
        for frmObj in frmObjs:
            frmObj.frame.x += self._border_padding
            frmObj.frame.y += self._border_padding
            frmObj.frame.w -= self._shape_padding
            frmObj.frame.h -= self._shape_padding

        return True

    def splitFreeRects(self, frmObj):
        to_be_del = []
        rect = copy.copy(frmObj.frame)
        if frmObj.rotated:
            rect.w, rect.h = rect.h, rect.w
        for i, r in enumerate(self.freeRects):
            if rect.x + rect.w <= r.x or rect.x >= r.x + r.w or rect.y + rect.h <= r.y or rect.y >= r.y + r.h:
                continue
            else:
                newpos = None
                if rect.x + rect.w > r.x and rect.x < r.x + r.w:
                    if rect.y > r.y:
                        newpos = PixelRect(r.x, r.y, r.w, rect.y - r.y)
                        self.freeRects.append(newpos)
                    elif rect.y + rect.h < r.y + r.h:
                        newpos = PixelRect(r.x, rect.y + rect.h, r.w, r.y + r.h - (rect.y + rect.h))
                        self.freeRects.append(newpos)
                if rect.y + rect.h > r.y and rect.y < r.y + r.h:
                    if rect.x > r.x:
                        newpos = PixelRect(r.x, r.y, rect.x - r.x, r.h)
                        self.freeRects.append(newpos)
                    elif rect.x + rect.w < r.x + r.w:
                        newpos = PixelRect(rect.x + rect.w, r.y, r.x + r.w - (rect.x + rect.w), r.h)
                        self.freeRects.append(newpos)
                if newpos is not None:
                    to_be_del.append(i)
        self._freeRects = [r for i, r in enumerate(self.freeRects) if i not in to_be_del]
        return bool(to_be_del)


