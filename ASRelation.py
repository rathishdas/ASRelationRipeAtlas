__author__ = 'RATHISH DAS and SARTHAK GHOSH'
#!/usr/bin/env python

import sys
import traceroute
import scc
jsonFile = sys.argv[1]
outFile = sys.argv[2]

if __name__ == '__main__':
    traceroute.getTraceRoute(jsonFile)
    scc.getRelation(outFile)
    print "AS relationship extracted !!!"
