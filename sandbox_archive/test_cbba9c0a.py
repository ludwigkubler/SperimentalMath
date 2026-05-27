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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

def rank(A):
    n = len(A)
    r = 0
    gaussian_elimination(A)
    for i in range(n):
        if all(abs(A[i][j]) < 1e-9 for j in range(r)):
            continue
        r += 1
    return r

def dpll_depth(clauses, assignment):
    if not clauses:
        return 0
    for literal in assignment:
        new_clauses = []
        for clause in clauses:
            if literal in clause or -literal in clause:
                continue
            new_clause = [l for l in clause if l != -literal]
            if new_clause:
                new_clauses.append(new_clause)
        return 1 + max(dpll_depth(new_clauses, assignment | {literal}), dpll_depth(new_clauses, assignment | {-literal}))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 3)
    
    clauses = []
    for _ in range(m):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(1, n))]
        if len(clause) > 1:
            random.shuffle(clause)
        clauses.append(tuple(sorted(clause)))
    
    assignment = set()
    depth = dpll_depth(clauses, assignment)
    
    # Construct tropicalized Lie algebra
    A = [[0] * n for _ in range(n)]
    for clause in clauses:
        for i in range(len(clause)):
            for j in range(i + 1, len(clause)):
                A[abs(clause[i]) - 1][abs(clause[j]) - 1] += 1
    
    rank_value = rank(A)
    
    if depth == 0:
        return {
            "metric_name": "Minimal Rank",
            "metric_value": rank_value,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "DPLL depth is zero, cannot compute ratio"
        }
    
    ratio = rank_value / depth
    conjecture_holds = math.log(depth) <= ratio
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": rank_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Ratio {ratio} > log({depth})"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")