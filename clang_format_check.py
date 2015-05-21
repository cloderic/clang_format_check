#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import glob
import os
import subprocess
import traceback
import xml.etree.ElementTree as ET

from collections import namedtuple
Replacement = namedtuple("Replacement", "offset length text")
Error = namedtuple("Error", "line column found expected")

__author__ = "github.com/cloderic"
__version__ = "0.2"

def replacements_from_file(file, style="file"):
    replacements = []

    clang_format_args = ["clang-format"]
    clang_format_args.append("-style={}".format(style))
    clang_format_args.append("-output-replacements-xml")
    clang_format_args.append(os.path.basename(file))
    replacement_xml = subprocess.check_output(clang_format_args, cwd = os.path.dirname(file))
    replacement_xml_root = ET.XML(replacement_xml)
    for replacement_item in replacement_xml_root.findall('replacement'):
        replacements.append(Replacement(
            offset = int(replacement_item.attrib["offset"]),
            length = int(replacement_item.attrib["length"]),
            text = replacement_item.text
        ))

    return replacements

def errors_from_replacements(file, replacements = []):
    errors = []

    lines = [0] # line index to character offset
    file_content = ""
    for line in open(file, "r"):
        file_content += line
        lines.append(lines[-1] + len(line))

    for line_index, line_offset in enumerate(lines[:-1]):
        while len(replacements) > 0 and lines[line_index + 1] > replacements[0].offset:
            replacement = replacements.pop(0)
            errors.append(Error(
                line = line_index,
                column = replacement.offset - line_offset,
                found = file_content[replacement.offset:replacement.offset + replacement.length],
                expected = replacement.text if replacement.text else ""
            ))

        if len(replacements) == 0:
            break

    return errors

def clang_format_check(
    files=[],
    style="file"):

    print "Checking {} files...".format(len(files))

    errorCount = 0
    file_errors = dict()

    for file in files:
        replacements = replacements_from_file(file, style)
        errors = errors_from_replacements(file, replacements)
        errorCount += len(errors)
        file_errors[file] = errors

    if errorCount == 0:
        print "No format error found"
    else:
        for file, errors in file_errors.iteritems():
            print "-- {} format errors at {}:".format(len(errors), file)
            for error in errors:
                print "    ({},{})".format(error.line + 1, error.column + 1)
                # print "        - found: \"{}\"".format(error.found)
                # print "        - expected: \"{}\"".format(error.expected)
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
        help="Coding style, pass-through to clang-format's -style=<string>, (default is '%(default)s').")

    # Exit cleanly on missing clang-format
    parser.add_argument("--success-on-missing-clang-format",
        action="store_true",
        help="If set this flag will lead to a success (zero exit status) if clang-format is not available.")

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
            if args.success_on_missing_clang_format:
                exit(0)
            else:
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
