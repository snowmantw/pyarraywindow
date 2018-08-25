import unittest
from window import Window, Index, IndexUnderflow, IndexOverflow, InvalidIndex

class TestArrayWindow(unittest.TestCase):
  
    def test_zero_length(self):
        self.assertRaises(InvalidIndex, lambda: Window([], 0, 0))

    def test_normal_range(self):
        Window([1], 0, 0)
        Window([1, 2], 0, 1)
        Window([1, 2, 3], 0, 1)
        Window([1, 2, 3], 1, 2)

    def test_overflow(self):
        self.assertRaises(IndexOverflow, lambda: Window([1], 0, 1))
        self.assertRaises(IndexOverflow, lambda: Window([1,2,3], 0, 6))
        self.assertRaises(IndexOverflow, lambda: Window([1,2,3], 1, 6))

    def test_underflow(self):
        self.assertRaises(IndexUnderflow, lambda: Window([1], -3, 0))

    def test_pivot(self):
        even = Window([99, 1,2,3,4, 99, 99], 1, 4)
        ep = even.pivot()
        
        # Even case: pivot + 1
        self.assertEqual(ep.index, 3)

        odd = Window([99, 1,2,4,5,6, 99, 99], 1,5)
        op = odd.pivot()

        # Odd case: pivot
        self.assertEqual(op.index, 3)

        one = Window([99, 1, 99], 1, 1)
        self.assertEqual(one.pivot().index, 1)

    def test_iter(self):
        even = Window([99, 1,2,3,4, 99, 99], 1, 4)
        eiter = iter(even)
        self.assertEqual(next(eiter), 1)
        self.assertEqual(next(eiter), 2)
        self.assertEqual(next(eiter), 3)
        self.assertEqual(next(eiter), 4)
        self.assertRaises(StopIteration, lambda: next(eiter))


    def test_split(self):
        even = Window([99, 1,2,3,4, 99, 99], 1, 4)
        (le, re) = even.split()
        self.assertSequenceEqual(le.to_array(), [1,2])
        self.assertSequenceEqual(re.to_array(), [3,4])

        odd = Window([99, 1,2,3,4,5, 99, 99], 1, 5)
        (lo, ro) = odd.split()
        self.assertSequenceEqual(lo.to_array(), [1,2])
        self.assertSequenceEqual(ro.to_array(), [3,4,5])

    def test_custom_split(self):
        even = Window([99, 1,2,3,4, 99, 99], 1, 4)
        epindex = Index(even, 2)  # Index not reset from zero
        (le, re) = even.split(epindex)
        self.assertSequenceEqual(le.to_array(), [1])
        self.assertSequenceEqual(re.to_array(), [2, 3, 4])

        odd = Window([99, 1,2,3,4,5, 99, 99], 1, 5)
        opindex = Index(odd, 2)  # Index not reset from zero
        (lo, ro) = odd.split(opindex)
        self.assertSequenceEqual(lo.to_array(), [1])
        self.assertSequenceEqual(ro.to_array(), [2,3,4,5])
        



if __name__ == '__main__':
  unittest.main()
