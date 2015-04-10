#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import subprocess

file_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
clang_format_check = os.path.join(file_dir, "..", "clang_format_check.py")

def execute(args):
    try:
        output = subprocess.check_output(args, cwd = file_dir)
        return 0, output
    except subprocess.CalledProcessError, e:
        return e.returncode, e.output

class TestClangFormatCheck(unittest.TestCase):
    def test_valid_files(self):
        for root, dirs, files in os.walk(file_dir):
            for file in files:
                if file[-6:-4] == "ok":
                    returncode, output = execute([clang_format_check, os.path.join(root, file)])
                    self.assertEqual(returncode, 0)

    def test_invalid_files(self):
        for root, dirs, files in os.walk(file_dir):
            for file in files:
                if file[-6:-4] == "ko":
                    returncode, output = execute([clang_format_check, os.path.join(root, file)])
                    self.assertNotEqual(returncode, 0)
                    self.assertEqual(output, open(os.path.join(root, file + ".out")).read())

    def test_fails_when_no_files(self):
        returncode, output = execute([clang_format_check])
        self.assertNotEqual(returncode, 0)
