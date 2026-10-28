#!/usr/bin/env python3
"""mkdimacs.py <raw_5lit.cnf> <out.dimacs>
raw format: first line 'n m K', then m lines of K literals.
out: standard DIMACS 'p cnf n m' + each clause terminated by 0."""
import sys

raw, out = sys.argv[1], sys.argv[2]
L = open(raw).read().split('\n')
n, m, K = map(int, L[0].split())
o = ['p cnf %d %d' % (n, m)]
for l in L[1:m + 1]:
    if l.strip():
        o.append(l.strip() + ' 0')
open(out, 'w').write('\n'.join(o) + '\n')
print('dimacs ok', n, m)
