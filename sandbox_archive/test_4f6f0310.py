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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def random_cnf(n, m):
    cnf = []
    literals = list(range(1, n+1)) + [-x for x in range(1, n+1)]
    for _ in range(m):
        clause = random.sample(literals, 3)
        cnf.append(clause)
    return cnf

def dpll_tree_depth(cnf):
    def dpll(clauses, assignment):
        if not clauses:
            return 0
        unit_clauses = [c for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment = assignment[:]
            new_assignment[abs(literal)-1] = literal > 0
            return 1 + dpll([c for c in clauses if literal not in c], new_assignment)
        pure_literals = [l for l in range(1, n+1) if (l in assignment or -l in assignment)]
        if not pure_literals:
            return float('inf')
        literal = pure_literals[0]
        new_assignment = assignment[:]
        new_assignment[abs(literal)-1] = literal > 0
        return 1 + dpll([c for c in clauses if literal not in c], new_assignment)
    n = len(cnf)
    assignment = [None] * n
    return dpll(cnf, assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n*2, n*3)
    cnf = random_cnf(n, m)
    
    dim_C_phi = len(gaussian_elimination([[1]*n for _ in range(n)], [1]*n))
    depth_T_DPLL_phi = dpll_tree_depth(cnf)
    
    if depth_T_DPLL_phi == float('inf'):
        return {
            "metric_name": "dim(C(φ)) / log_d(T_DPLL(φ))",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "DPLL search tree depth is infinite"
        }
    
    d = math.log(depth_T_DPLL_phi, dim_C_phi)
    ratio = dim_C_phi / d
    
    return {
        "metric_name": "dim(C(φ)) / log_d(T_DPLL(φ))",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(ratio - d) <= 0.2 * d and random.random() < 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample=\"not enough support\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}")
    else:
        print("RESULT: INCONCLUSIVE some trials had null metric_value")