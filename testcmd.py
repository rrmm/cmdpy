#!/usr/bin/python3

import sys
from collections import namedtuple
from cmd import Cmd, CountLines, Filter, LineFilter, Result, LResult


#c=Cmd("./test_gen.py") | Cmd("./wait.py")
#c.exec()


class TestGen(Filter):
    def process(process, stdin, stdout, stderr):
        total=0
        for i in range(0, 100):
            total += stdout.write(" ".join(['a']*512))
            sys.stderr.write(f"{i} {total}\n")
        # end for
    # end def
# end


c= TestGen() | Cmd("./wait.py")
c.exec()
