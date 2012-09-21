# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys #as __sys

class vlogger:
    def __init__(self, verbosity = 0, log = sys.stderr):
        self.__verbosity = verbosity
        self.__log = log
    
    def __call__(self, verbosity, msg):
        if verbosity <= self.__verbosity:
            print(self.__log, '*' * verbosity, msg)