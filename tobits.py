#!/usr/bin/env python3
"""tobits.py <solver_output_with_v_lines>
Reads SAT-solver output (kissat/cms/minisat) and prints the assignment as
exactly n chars of 0/1 (char k-1 = variable k). n comes from the max var seen."""
import sys

vals = {}
for line in open(sys.argv[1]):
    line = line.strip()
    if line.startswith('v ') or (line and line[0] in 'v'):
        body = line[1:] if line[0] == 'v' else line
        for tok in body.split():
            try:
                i = int(tok)
            except ValueError:
                continue
            if i:
                vals[abs(i)] = '1' if i > 0 else '0'
if not vals:
    sys.exit(1)
n = max(vals)
print(''.join(vals.get(k, '0') for k in range(1, n + 1)))
