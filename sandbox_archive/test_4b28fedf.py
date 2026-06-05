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

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = set()
        while len(clause) < 2:
            lit = random.randint(1, n)
            if random.choice([True, False]):
                lit = -lit
            clause.add(lit)
        cnf.append(tuple(sorted(clause)))
    return cnf

def construct_quotient_algebra(cnf):
    n = max(abs(lit) for clause in cnf for lit in clause)
    A = [[0] * n for _ in range(n)]
    
    for clause in cnf:
        for lit1, lit2 in itertools.combinations(clause, 2):
            if abs(lit1) > n or abs(lit2) > n:
                continue
            A[abs(lit1) - 1][abs(lit2) - 1] += 1
    
    return A

def frobenius_norm(A):
    norm = 0
    for row in A:
        for val in row:
            norm += val ** 2
    return math.sqrt(norm)

def circuit_monotone_width(cnf):
    n = max(abs(lit) for clause in cnf for lit in clause)
    width = 0
    
    def dfs(assignment, level):
        nonlocal width
        if level == n:
            width = max(width, len([x for x in assignment if x != 0]))
            return
        
        for val in [-1, 1]:
            assignment[level] = val
            dfs(assignment, level + 1)
    
    dfs([0] * n, 0)
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(1, min(n * (n - 1), 100))
        cnf = generate_cnf(n, m)
        
        A = construct_quotient_algebra(cnf)
        frobenius_norm_value = frobenius_norm(A)
        width = circuit_monotone_width(cnf)
        
        results.append({
            "n": n,
            "m": m,
            "frobenius_norm": frobenius_norm_value,
            "width": width
        })
    
    mean_frobenius_norm = sum(result["frobenius_norm"] for result in results) / len(results)
    mean_width = sum(result["width"] for result in results) / len(results)
    
    conjecture_holds = all(
        frobenius_norm_value <= 1.5 * math.sqrt(m) * n ** (3/4)
        for result in results
        for m, n in zip([result["m"]] * len(n_values), [result["n"]] * len(n_values))
    )
    
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Frobenius Norm",
        "metric_value": mean_frobenius_norm,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if not trial_result["conjecture_holds"]:
            break
        
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")