# -*- coding: utf-8 -*-
# ===================================
# ScriptName : test_unittest.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-01-18 17:16
# ===================================

import unittest

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
    # 可以使用下面的2行代替 unittest.main()
    # suite = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
    # unittest.TextTestRunner(verbosity=2).run(suite)
    