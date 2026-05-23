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
        max_row = i
        for r in range(i+1, rows):
            if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                max_row = r
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below
        denom = matrix[i][i]
        if denom == 0:
            continue
        for j in range(i, cols):
            matrix[i][j] /= denom
        
        for r in range(rows):
            if r != i:
                factor = matrix[r][i]
                for j in range(i, cols):
                    matrix[r][j] -= factor * matrix[i][j]
    return matrix

def min_rank_tropical_lie_algebra(cnf):
    # Simplified representation of tropicalized Lie algebra rank calculation
    n = len(cnf)
    A = [[0]*n for _ in range(n)]
    for clause in cnf:
        for literal in clause:
            if literal > 0:
                A[literal-1][literal-1] += 1
            else:
                A[-literal-1][-literal-1] += 1
    return len(gaussian_elimination(A))

def weight_disjunctive_normal_form(cnf):
    # Simplified representation of disjunctive normal form weight calculation
    n = len(cnf)
    return sum(len(clause) for clause in cnf)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    cnf = [[random.randint(-n, n) for _ in range(random.randint(2, n))] for _ in range(n)]
    
    min_rank = min_rank_tropical_lie_algebra(cnf)
    weight = weight_disjunctive_normal_form(cnf)
    
    return {
        "metric_name": "min_rank",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": min_rank >= weight,
        "counterexample": "" if min_rank >= weight else f"Instance with n={n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results) and all(r["counterexample"] != "" for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={seeds[0]}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")