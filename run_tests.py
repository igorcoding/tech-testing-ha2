#!/usr/bin/env python2

import sys
import unittest
from tests import ad_edit_test
from tests.ad_creation_test import AdCreationTest


if __name__ == '__main__':
    suite = unittest.TestSuite((
        unittest.makeSuite(AdCreationTest),
        unittest.makeSuite(ad_edit_test),
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())