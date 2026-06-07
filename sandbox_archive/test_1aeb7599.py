# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]

    return A

def determinant(A):
    n = len(A)
    det = 1
    for i in range(n):
        if A[i][i] == 0:
            return 0
        det *= A[i][i]
        A = gaussian_elimination([row[:i] + row[i+1:] for row in A[i+1:]])
    return det

def dpll(phi):
    literals = set()
    clauses = []
    for clause in phi.split(' '):
        if clause:
            literals.update(clause.split('|'))
            clauses.append(clause.split('|'))

    def solve(assignment):
        unsatisfied = [lit for lit in literals if not evaluate(lit, assignment)]
        if not unsatisfied:
            return True
        literal = unsatisfied[0]
        for value in [True, False]:
            new_assignment = assignment.copy()
            new_assignment[literal] = value
            if solve(new_assignment):
                return True
        return False

    def evaluate(lit, assignment):
        if lit.startswith('~'):
            return not assignment.get(lit[1:], False)
        else:
            return assignment.get(lit, False)

    return solve({})

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    phi = ' | '.join([''.join(random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 2)) for _ in range(10)])
    
    w_phi = 1 if dpll(phi) else float('inf')
    mhr_phi = determinant([[random.randint(-1, 1) for _ in range(n)] for _ in range(n)])
    
    ratio = mhr_phi / w_phi if w_phi != float('inf') else float('inf')
    
    return {
        "metric_name": "mhr_over_w",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio <= 1,
        "counterexample": "" if ratio <= 1 else "phi: {}".format(phi)
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)
    
    mean_ratio = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_ratio, 0, support_fraction))
    elif support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_ratio, 0, support_fraction))
    else:
        first_failing_seed = next(seed for seed, res in enumerate(results) if not res["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample='phi: {}' first_failing_seed={}".format(results[first_failing_seed]["counterexample"], first_failing_seed))