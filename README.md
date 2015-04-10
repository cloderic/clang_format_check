# clang-format check #

:construction: _Still a work in progress, contributions are welcome_ :construction:

[![Build Status](https://travis-ci.org/cloderic/clang_format_check.svg?branch=master)](https://travis-ci.org/cloderic/clang_format_check)

In the spirit of linter and coding style checker such as [jshint](http://jshint.com) or [jscs](http://jscs.info), this helper script relies on [clang-format](http://clang.llvm.org/docs/ClangFormat.html) to check and report coding style issues in C and C++ codebases.

    usage: clang_format_check.py [-h] [-s STYLE]
                                 [--success-on-missing-clang-format]
                                 file [file ...]

    C/C++ formatting check using clang-format

    positional arguments:
      file                  Paths to the files that'll be checked (wilcards
                            accepted).

    optional arguments:
      -h, --help            show this help message and exit
      -s STYLE, --style STYLE
                            Coding style, pass-through to clang-format's
                            -style=<string>, (default is 'file').
      --success-on-missing-clang-format
                            If set this flag will lead to a success (zero exit
                            status) if clang-format is not available.

## Install dependencies ##

Run the usual `pip install -r requirements.txt`

## Running tests ##

Simply run [`nosetests`](https://nose.readthedocs.org) to launch the script on all `.cpp` files under `test/data`.

- All tests are run with the _file_ style, they'll rely on their `.clang-format` file.
- All files ending with `...ok.cpp` should be valid.
- All files ending with `...ko.cpp` should be invalid, the tool outputs should match the accompanying `...ko.cpp.out`.
