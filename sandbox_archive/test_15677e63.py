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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def compute_hecke_algebra(f):
    n = int(math.log2(len(f)))
    H = [[0] * (2**n) for _ in range(2**n)]
    for i in range(2**n):
        for j in range(2**n):
            if f[i ^ j] == 1:
                H[i][j] = 1
    return H

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def rank_of_matrix(A):
    A = gaussian_elimination(A)
    rank = 0
    for row in A:
        if any(row):
            rank += 1
    return rank

def compute_frege_depth(f):
    n = int(math.log2(len(f)))
    depth = 0
    while n > 1:
        n = (n + 1) // 2
        depth += 1
    return depth

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for _ in range(30):
        f = generate_boolean_function(random.randint(5, 40))
        H = compute_hecke_algebra(f)
        rho_H = rank_of_matrix(H)
        d = compute_frege_depth(f)
        results.append((rho_H, d))
    
    total_rho_H = sum(rho_H for rho_H, _ in results)
    total_d = sum(d for _, d in results)
    mean_rho_H = Fraction(total_rho_H).limit_denominator()
    mean_d = Fraction(total_d).limit_denominator()
    ratio = mean_rho_H / mean_d
    
    conjecture_holds = ratio > Fraction(3, 2)
    counterexample = "" if conjecture_holds else f"mean_ratio={ratio}"
    
    return {
        "metric_name": "rank_ratio",
        "metric_value": float(ratio),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, ...{trial_result}...}}")
        results.append(trial_result)
    
    total_rho_H = sum(rho_H for rho_H, _ in [res["metric_value"] for res in results])
    total_d = sum(d for _, d in [res["instances_tested"] for res in results])
    mean_ratio = Fraction(total_rho_H).limit_denominator() / Fraction(total_d).limit_denominator()
    
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")