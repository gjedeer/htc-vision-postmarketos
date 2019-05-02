import sys

with open(sys.argv[1]) as f:
    while True:
        b = f.read(1)
        print "%04x\t%d\t%s" % (ord(b), ord(b), b)
