#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import dwz
import unittest


class DwzTestCase(unittest.TestCase):
    def test_check_tov(self):
        # valid
        for tov in ("1-year", "long-term"):
            self.assertIsNone(dwz.check_tov(tov), "valid term of validity")

        # invalid
        for tov in ("", "1-month"):
            self.assertRaises(ValueError, dwz.check_tov, tov)

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
                print("Expected Error raised for {}".format(long))


if __name__ == '__main__':
    unittest.main()
