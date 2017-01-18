# -*- coding: utf-8 -*-
# ===================================
# ScriptName : test_unittest.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-01-18 17:16
# ===================================

import random
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)
        print "call setup"

    def tearDown(self):
        print "call teardown"

    def test_shuffle(self):
        # make sure the shuffled sequence does not lose any elements
        random.shuffle(self.seq)
        self.seq.sort()
        self.assertEqual(self.seq, range(10))

        # should raise an exception for an immutable sequence
        self.assertRaises(TypeError, random.shuffle, (1,2,3))

    def test_choice(self):
        element = random.choice(self.seq)
        self.assertTrue(element in self.seq)

    def test_sample(self):
        with self.assertRaises(ValueError):
            random.sample(self.seq, 20)
        for element in random.sample(self.seq, 5):
            self.assertTrue(element in self.seq)

if __name__ == '__main__':
    unittest.main()
    # 可以使用下面的2行代替 unittest.main()
    # suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
    # unittest.TextTestRunner(verbosity=2).run(suite)
    