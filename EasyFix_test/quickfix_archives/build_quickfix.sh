#!/usr/bin/env zsh

# cd to the unzipped quickfix folder
cd quickfix_archives/quickfix-1.15.1-M1Build || exit

#if not installed install llvm
#brew install llvm

#run the quickfix setup install for the version of python (3.8+)
python setup.py install
