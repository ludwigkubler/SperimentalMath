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
    m, n = len(A), len(A[0])
    for i in range(m):
        pivot_row = i
        for j in range(i + 1, m):
            if abs(A[j][i]) > abs(A[pivot_row][i]):
                pivot_row = j
        A[i], A[pivot_row] = A[pivot_row], A[i]
        if A[i][i] == 0:
            continue
        for j in range(i + 1, m):
            factor = -A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] += factor * A[i][k]

def min_rank(matrix):
    rank = len(matrix)
    gaussian_elimination(matrix)
    for row in matrix:
        if all(cell == 0 for cell in row):
            rank -= 1
    return rank

def p_adic_diff(clause, n):
    diff = [Fraction(0) for _ in range(n + 1)]
    for literal in clause:
        if literal > 0:
            diff[literal] += Fraction(1)
        else:
            diff[-literal] -= Fraction(1)
    return diff

def generate_cnf(n, m):
    cnf = []
    variables = list(range(1, n + 1))
    for _ in range(m):
        clause = random.sample(variables, random.randint(1, n))
        cnf.append(clause)
    return cnf

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = n * 2
    cnf = generate_cnf(n, m)
    
    p_adic_diffs = []
    for clause in cnf:
        diff = p_adic_diff(clause, n)
        p_adic_diffs.extend(diff)
    
    rank = min_rank([p_adic_diffs[i:i+n+1] for i in range(0, len(p_adic_diffs), n + 1)])
    
    expected_rank = math.isqrt(n) * 1.5
    conjecture_holds = expected_rank - 1.5 <= rank <= expected_rank + 1.5
    
    return {
        "metric_name": "min_rank",
        "metric_value": rank,
        "instances_tested": len(cnf),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"rank={rank}, expected={expected_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank exceeds expected\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")