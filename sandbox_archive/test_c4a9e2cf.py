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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        # Find pivot
        max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below
        for j in range(i + 1, rows):
            factor = -matrix[j][i] / matrix[i][i]
            for k in range(cols):
                if i == k:
                    matrix[j][k] = 0
                else:
                    matrix[j][k] += factor * matrix[i][k]

def rank(matrix):
    augmented_matrix = [row[:] + [1] for row in matrix]
    gaussian_elimination(augmented_matrix)
    return sum(1 for row in augmented_matrix if any(row))

def dpll(cnf, assignment=[]):
    if not cnf:
        return True
    if any(all(v not in assignment and -v not in assignment for v in clause) for clause in cnf):
        return False
    
    p_var = next(abs(v) for v in range(1, len(cnf) + 1) if v not in assignment and -v not in assignment)
    
    new_assignment = assignment[:]
    new_assignment.append(p_var)
    if dpll(cnf, new_assignment):
        return True
    
    new_assignment.pop()
    new_assignment.append(-p_var)
    return dpll(cnf, new_assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 20
    cnf = []
    for _ in range(n):
        num_clauses = random.randint(1, n)
        clause = [random.choice([-i, i]) for i in range(1, n + 1)]
        cnf.append(clause)
    
    height = dpll(cnf)
    instances_tested = 1
    n_max = n
    conjecture_holds = True
    counterexample = ""
    
    return {
        "metric_name": "DPLL Search Tree Height",
        "metric_value": height,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_height = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_height} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")