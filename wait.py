#!/usr/bin/python3

import sys
import time


time.sleep(5)
total = 0
while 1:
    val = sys.stdin.read(1024)
    res = len(val)
    total += res
    if (val==""):
        break
    # end if
    sys.stderr.write(f"read {res} total: {total}\n")
    time.sleep(1)
# end while
