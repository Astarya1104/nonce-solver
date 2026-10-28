#!/usr/bin/env python3
"""verify.py <dimacs.cnf> <solution.txt>
Exit 0 if the 0/1 assignment satisfies every clause."""
import sys

cnf, sol = sys.argv[1], sys.argv[2]
clauses = []
for line in open(cnf):
    line = line.strip()
    if not line or line[0] in 'cp':
        continue
    lits = [int(x) for x in line.split() if x != '0']
    if lits:
        clauses.append(lits)
a = open(sol).read().strip()
if not a or set(a) - set('01'):
    print("BAD assignment chars")
    sys.exit(1)
bad = 0
for lits in clauses:
    if not any((x > 0) == (a[abs(x) - 1] == '1') for x in lits):
        bad += 1
print("clauses=%d unsat=%d len=%d" % (len(clauses), bad, len(a)))
sys.exit(0 if bad == 0 else 1)
