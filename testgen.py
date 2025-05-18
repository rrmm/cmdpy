#!/usr/bin/python3

import sys

total=0
for i in range(0, 100):
    total += sys.stdout.write(" ".join(['a']*512))
    sys.stderr.write(f"{i} {total}\n")
# end
