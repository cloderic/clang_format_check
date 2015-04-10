#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import glob
import os
import subprocess
import traceback
import xml.etree.ElementTree as ET

from collections import namedtuple
Error = namedtuple("Error", "line column length expected")

__author__ = "github.com/cloderic"
__version__ = "0.1"

def countbytes(iterable):
    bytes = 0
    for item in iterable:
        bytes += len(item)
        yield bytes

def linecolumn_from_offset(file, offset):
    line_count = 0
    previous_byte_count = 0
    byte_count = 0
    for line in open(file, "r"):
        line_count += 1
        byte_count += len(line)
        if byte_count > offset:
            return line_count, offset - previous_byte_count
        previous_byte_count = byte_count
    raise Exception("Can't reach byte #{} in '{}'".format(offset, file))

def clang_format_check(
    files=[],
    style="file"):

    print "Checking {} files...".format(len(files))

    errorCount = 0
    file_errors = dict()

    for file in files:
        clang_format_args = ["clang-format"]
        clang_format_args.append("-style={}".format(style))
        clang_format_args.append("-output-replacements-xml")
        clang_format_args.append(os.path.basename(file))
        replacement_xml = subprocess.check_output(clang_format_args, cwd = os.path.dirname(file))
        replacement_xml_root = ET.XML(replacement_xml)
        for replacement in replacement_xml_root.findall('replacement'):
            offset = int(replacement.attrib["offset"])
            line, column = linecolumn_from_offset(file, offset)
            error = Error(
                line = line,
                column = column,
                length = int(replacement.attrib["length"]),
                expected = replacement.text
            )
            errorCount += 1
            if file in file_errors:
                file_errors[file].append(error)
            else:
                file_errors[file] = [error]

    if errorCount == 0:
        print "No format error found"
    else:
        for file, errors in file_errors.iteritems():
            print "-- {} format errors at {}:".format(len(errors), file)
            for error in errors:
                print "    ({},{})".format(error.line, error.column)
        print "---"
        print "A total of {} format errors were found".format(errorCount)
    return errorCount, file_errors

def check_clang_format_exec():
    try:
        subprocess.check_output(["clang-format", "-version"])
        return True
    except subprocess.CalledProcessError, e:
        # it seems that in some version of clang-format '-version' leads to non-zero exist status
        return True
    except OSError, e:
        return False

def main():
    parser = argparse.ArgumentParser(description="C/C++ formatting check using clang-format")

    # Style
    parser.add_argument("-s", "--style",
        default="file",
        help="Coding style, pass-through to clang-format's -style=<string>, (default is '%(default)s')")

    # Files or directory to check
    parser.add_argument("file", nargs="+", help="Paths to the files that'll be checked (wilcards accepted).")
    args = parser.parse_args()

    try:
        # Adding the double quotes around the inline style
        if len(args.style) > 0 and args.style[0] == "{":
            args.style = "\"" + args.style + "\""

        # Checking that clang-format is available
        if not check_clang_format_exec():
            print "Can't run 'clang-format', please make sure it is installed and reachable in your PATH."
            exit(-1)

        # globing the file paths
        files = set()
        for pattern in args.file:
            for file in glob.iglob(pattern):
                files.add(os.path.relpath(file))

        errorCount, file_errors = clang_format_check(style=args.style, files=list(files))
        exit(errorCount)

    except Exception, e:
        print "Exception raised:"
        print "    " + str(e)
        print '-'*60
        traceback.print_exc()
        print '-'*60
        exit(-2)

if __name__ == "__main__" :
    main()
