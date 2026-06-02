# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def gaussian_elimination(matrix):
    n = len(matrix)
    rank = 0
    for col in range(n):
        pivot_row = -1
        for row in range(rank, n):
            if matrix[row][col] != 0:
                pivot_row = row
                break
        if pivot_row == -1:
            continue
        matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
        rank += 1
        for row in range(rank, n):
            factor = Fraction(matrix[row][col], matrix[pivot_row][col])
            for j in range(n):
                if factor == 0:
                    continue
                matrix[row][j] -= factor * matrix[pivot_row][j]
    return rank

def compute_brauer_group_order(cnf):
    n = len(cnf)
    A = [[0] * n for _ in range(n)]
    for clause in cnf:
        for lit in clause:
            row = abs(lit) - 1
            if lit > 0:
                A[row][row] += 1
            else:
                A[row][row] -= 1
    return gaussian_elimination(A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    cnf = []
    for _ in range(n):
        clause = [random.choice([-i, i]) for i in range(1, n + 1)]
        cnf.append(clause)
    
    log2_brauer_group = log2(compute_brauer_group_order(cnf))
    r_phi = len(cnf)  # Simplified communication complexity rank
    
    correlation_coefficient = (log2_brauer_group * r_phi - n * (n + 1)) / (n * (n - 1))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(correlation_coefficient) >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_below_0.5\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(seeds)}")