# clang-format check #

:construction: _Still a work in progress, contributions are welcome_ :construction:

[![Build Status](https://travis-ci.org/cloderic/clang_format_check.svg?branch=master)](https://travis-ci.org/cloderic/clang_format_check)

Coding style checker relying on [clang-format](http://clang.llvm.org/docs/ClangFormat.html).

    usage: clang_format_check.py [-h] [-s STYLE] file [file ...]

    C/C++ formatting check using clang-format

    positional arguments:
      file                  Paths to the files that'll be checked (wilcards
                            accepted).

    optional arguments:
      -h, --help            show this help message and exit
      -s STYLE, --style STYLE
                            Coding style, pass-through to clang-format's
                            -style=<string>, (default is 'file')

## Running tests ##

Simply run `./test/run_tests.py` to launch the script on all `.cpp` files under `test/data`.

- All tests are run with the _file_ style, they'll rely on their `.clang-format` file.
- All files ending with `...ok.cpp` should be valid.
- All files ending with `...ko.cpp` should be invalid, the tool outputs should match the accompanying `...ko.cpp.out`.
