#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import unittest

import dwz
from dwz import TOV


class DwzTestCase(unittest.TestCase):
    def test_TOV_check(self):
        # valid
        for tov in (TOV.ONE_YEAR, TOV.LONG_TERM):
            self.assertIsNone(TOV.check(tov), "valid term of validity")

        # invalid
        for tov in ("", "1-month", "1-year", "long-term"):
            with self.assertRaises(ValueError):
                TOV.check(tov)
                print("Expected Error raised for {}.".format(tov))

    def test_check_long_url(self):
        # valid
        for long in ("https://www.baidu.com/", "http://www.baidu.com"):
            self.assertIsNone(dwz.check_long_url(long), "valid long URL")

        # invalid scheme
        for long in ("", "www.baidu.com", "ftp://www.baidu.com"):
            self.assertRaises(ValueError, dwz.check_long_url, long)

        # invalid host
        for long in ("http://10.10.10.10:443/", "http://[FEDC:BA98:7654:3210:FEDC:BA98:7654:3210]:80/"):
            with self.assertRaises(ValueError):
                dwz.check_long_url(long)
                print("Expected Error raised for {}.".format(long))


if __name__ == '__main__':
    unittest.main()
