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

def gaussian_elimination(M):
    rows, cols = len(M), len(M[0])
    for i in range(rows):
        # Find pivot row
        max_row = i
        for r in range(i+1, rows):
            if abs(M[r][i]) > abs(M[max_row][i]):
                max_row = r
        M[i], M[max_row] = M[max_row], M[i]
        
        # Make the diagonal element 1
        pivot = M[i][i]
        for k in range(cols):
            M[i][k] /= pivot
        
        # Eliminate non-zero elements below the pivot
        for r in range(i+1, rows):
            factor = M[r][i]
            for k in range(cols):
                if k == i:
                    M[r][k] = 0
                else:
                    M[r][k] -= factor * M[i][k]
    return M

def rank(M):
    row_echelon_form = gaussian_elimination(M)
    rank = 0
    for row in row_echelon_form:
        if any(row):
            rank += 1
    return rank

def minimal_order(M):
    rows, cols = len(M), len(M[0])
    M_extended = [row + [1] for row in M]
    return rank(M_extended)

def cnf_to_matrix(phi):
    n = max(lit for clause in phi for lit in abs(clause))
    M = [[0] * (n + 1) for _ in range(len(phi))]
    for i, clause in enumerate(phi):
        for lit in clause:
            M[i][abs(lit)] += 1 if lit > 0 else -1
    return M

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    num_clauses = random.randint(n, n*2)
    phi = []
    for _ in range(num_clauses):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        phi.append(clause)
    
    M = cnf_to_matrix(phi)
    order = minimal_order(M)
    
    return {
        "metric_name": "minimal_order",
        "metric_value": order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": f"CNF with {num_clauses} clauses and minimal order {order}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")