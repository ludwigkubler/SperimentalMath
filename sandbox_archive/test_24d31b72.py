# auto-injected by SEC sandbox
import itertools
import collections
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
import json

def generate_unsat_cnf(n, m):
    literals = list(range(1, n + 1)) + [-l for l in range(1, n + 1)]
    clauses = set()
    while len(clauses) < m:
        clause = []
        for _ in range(3):
            l = random.choice(literals)
            if -l not in clause and l not in clause:
                clause.append(l)
        if any(l in clause for clause in clauses):
            continue
        clauses.add(tuple(sorted(clause)))
    return list(clauses)

def walsh_hadamard_transform(k_F):
    n = len(k_F)
    k_F.extend([0] * (2**n - len(k_F)))
    for s in range(1, n + 1):
        mask = (1 << s) - 1
        for i in range(2**(n-s)):
            j = i ^ mask
            k_F[i] += k_F[j]
            k_F[j] -= k_F[i]
    return [x / 2**s for s in range(n)]

def compute_fourier_variance_ratio(k_F):
    mean_k_F = sum(k_F) / len(k_F)
    variance = sum((k - mean_k_F)**2 for k in k_F) / len(k_F)
    k_F_hat = walsh_hadamard_transform(k_F)
    return (sum(k**2 for k in k_F_hat[1:]) / k_F_hat[0]**2)

def compute_tree_resolution_depth(F):
    n = int(math.log2(len(F)))
    memo = {}
    
    def dp(partial_assignment):
        hash_value = hash(tuple(sorted(partial_assignment.items())))
        if hash_value in memo:
            return memo[hash_value]
        empty_clause = any(l not in partial_assignment for clause in F)
        if empty_clause:
            return 0
        max_depth = 0
        for l, value in partial_assignment.items():
            new_assignment = partial_assignment.copy()
            new_assignment[l] = 1 - value
            depth = dp(new_assignment) + 1
            if depth > max_depth:
                max_depth = depth
        memo[hash_value] = max_depth
        return max_depth
    
    return dp({})

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [8, 10, 12, 14]
    m_over_n = 4.26
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        m = int(m_over_n * n)
        F = generate_unsat_cnf(n, m)
        
        k_F = [sum(1 for clause in F if l not in clause) for l in range(1, 2*n + 1)]
        R_F = compute_fourier_variance_ratio(k_F)
        d_T_F = compute_tree_resolution_depth(F)
        
        instances_tested += 1
        
        expected_bound = math.ceil(math.log2(1 / R_F)) + 1
        if d_T_F < expected_bound:
            conjecture_holds = False
            counterexample = f"n={n}, m={m}, d_T(F)={d_T_F}, expected_bound={expected_bound}"
    
    return {
        "metric_name": "tree_resolution_depth",
        "metric_value": d_T_F,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")