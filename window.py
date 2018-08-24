
class IndexOverflow(Exception):
    pass

class IndexUnderflow(Exception):
    pass

class InvalidIndex(Exception):
    pass

# Rules: Window and Index only accept integer as the init index,
# while methods of Window always return Index, not plain int.

class Index():

    def __init__(self, window, index):
        if index < window.minx:
            raise IndexUnderflow("Index underflow: %d < %d" % (index, window.minx))

        if index > window.maxx:
            raise IndexOverflow("Index overflow: %d > %d" % (index, window.maxx))

        self.index = index
        self.window = window

    def __sub__(self, offset):
        if self.index - offset < self.window.minx:
            raise IndexUnderflow("Index expression underflow: %d - %d < %d" % (index, offset, window.minx))

        self.index -= offset
        return self

    def __add__(self, offset):
        # Well python support infinite long number but still get used to do this (from addition to substraction)
        if self.index < self.window.maxx - offset:
            raise IndexOverflow("Index expression underflow: %d + %d > %d" % (index, offset, window.maxx))

        # And if we really need to check overflow, put it here
        # 
        # So that this line don't need to check it again.
        self.index += offset
        return self


class Window():

    def __init__(self, origin, min_index, max_index):
        if len(origin) == 0:
            raise InvalidIndex("Cannot make a window from zero-sized origin")
        if min_index < 0:
            raise IndexUnderflow("Min index < 0: %d" % min_index)
        if max_index < 0:
            raise IndexUnderflow("Max index < 0: %d" % max_index)
        if max_index >= len(origin):
            raise IndexOverflow("Max index out of range: %d > %d" % (max_index, len(origin)))
        if max_index < min_index:
            raise InvalidIndex("Max index < min index: %d < %d" % (max_index, min_index))

        self.minx = min_index
        self.maxx = max_index
        self.lenx = max_index - min_index + 1
        self.origin = origin

    # For even number, it will be [pivot+1]
    def pivot(self):
        olen = len(self.origin)
        if olen == 0:
            return None
        if olen == 1:
            return Index(self, self.minx)

        # index: 3,4,5,6,7 -> 3 + 5 // 2 = 3 + 2 = 5, pivot at index 5
        # index: 3,4,5,6   -> 3 + 4 // 2 = 3 + 2 = 5, pivot at index 5
        # index: 3,4       -> 3 + 2 // 2 = 3 + 1 = 4, pivot at index 4
        return Index(self, self.minx + self.lenx // 2)

    # return (minx -> [pivot - 1], [pivot] -> maxx)
    def split(self, pindex=None):
        if pindex == None:
            # half-half
            pindex = self.pivot()

        if self.lenx == 0:
            return None
        if self.lenx == 1:
            return (None, Window(self.origin, self.minx, self.maxx))

        lpart = Window(self.origin, self.minx, (pindex - 1).index)
        rpart = Window(self.origin, pindex.index, self.maxx)
        return (lpart, rpart)

Window([], 0, 0)
Window([1], 0, 0)
Window([1], 0, 1)
Window([1, 2], 0, 1)
Window([1, 2, 3], 0, 1)
Window([1, 2, 3], 0, 6)
Window([1, 2, 3], 1, 2)
Window([1, 2, 3], 1, 6)
