#!/usr/bin/env python2

import sys
import unittest
from tests.target_mail_test import TargetMailRuTest


if __name__ == '__main__':
    suite = unittest.TestSuite((
        unittest.makeSuite(TargetMailRuTest),
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())