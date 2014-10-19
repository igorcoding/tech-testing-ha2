#!/usr/bin/env python2
import os

import sys
import unittest
from datetime import datetime
from tests.ad_creation_test import AdCreationTest
from tests.ad_edit_test import AdEditTest

tests_dir = os.path.join(os.path.dirname(__file__), 'tests')
sys.path.insert(0, tests_dir)

if __name__ == '__main__':
    suite = unittest.TestSuite((
        unittest.makeSuite(AdCreationTest),
        unittest.makeSuite(AdEditTest),
    ))
    begin_time = datetime.now()
    result = unittest.TextTestRunner(verbosity=3).run(suite)
    end_time = datetime.now()

    td = end_time - begin_time
    minutes, seconds = td.seconds // 60 % 60, td.seconds

    print "Execution Time : %d min = %d s" % (minutes, seconds)
    sys.exit(not result.wasSuccessful())
