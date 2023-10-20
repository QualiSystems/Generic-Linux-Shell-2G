#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from driver import GenericLinuxOSShellDriver


class TestGenericLinuxShellDriver(unittest.TestCase):
    def setUp(self):
        self._instance = GenericLinuxOSShellDriver()

    def test_init(self):
        self.assertIsNone(self._instance._cli)
