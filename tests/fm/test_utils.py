from __future__ import absolute_import

import os
import unittest

os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'

from fixture_magic.utils import reorder_json

__author__ = 'davedash'



class UtilsTestCase(unittest.TestCase):
    def test_reorder_json(self):
        """Test basic ordering of JSON/python object."""
        input_json = [{'model': 'f'}, {'model': 'x'},]
        expected = [{'model': 'x'}, {'model': 'f'}]
        self.assertEqual(expected, reorder_json(input_json, models=['x', 'f'])
        )
