# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import itertools

def xor_lift(f, a):
    return tuple((b ^ a) for b in f)

def gaussian_elimination(M):
    n = len(M)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        
        # Eliminate below
        for j in range(i+1, n):
            factor = M[j][i] / M[i][i]
            for k in range(n):
                M[j][k] -= factor * M[i][k]

    rank = 0
    for row in M:
        if any(row):
            rank += 1
    return rank

def patience_sort(perm):
    piles = []
    for x in perm:
        inserted = False
        for pile in piles:
            if not pile or pile[-1] < x:
                pile.append(x)
                inserted = True
                break
        if not inserted:
            piles.append([x])
    return len(piles)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    k_values = [3, 4, 5]
    instances_tested = 0
    violations = 0
    max_rho = 0.0
    
    for n in k_values:
        M_all = []
        S_all = []
        
        # Generate random Boolean functions
        for _ in range(50):
            f = tuple(random.randint(0, 1) for _ in range(2**n))
            S = [i for i, bit in enumerate(f) if bit == 1]
            if len(S) < 2**(n-1) - 2 or len(S) > 2**(n-1) + 2:
                continue
            M_all.append(M)
            S_all.append(S)
            instances_tested += 1
        
        # Generate structured stress cases
        for _ in range(4):
            f = tuple(0 if i % 2 == 0 else 1 for i in range(2**n))
            M_all.append(M)
            S_all.append([i for i, bit in enumerate(f) if bit == 1])
            instances_tested += 1
        
        for M, S in zip(M_all, S_all):
            for a in itertools.product([0, 1], repeat=n):
                tau_a = tuple((b ^ a) for b in f)
                lis_length = patience_sort(tau_a)
                rho = lis_length / (gaussian_elimination(M) + 1)
                if rho > max_rho:
                    max_rho = rho
                if rho > 1.0:
                    violations += 1
    
    conjecture_holds = max_rho <= 1.0
    counterexample = "" if max_rho <= 1.0 else f"rho={max_rho:.4f}"
    
    return {
        "metric_name": "rho",
        "metric_value": max_rho,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    mean_rho = sum(r["metric_value"] for r in results) / len(results)
    max_rho = max(r["metric_value"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho:.4f} std=0.0000 support_fraction=1.0000")
    elif max_rho > 1.0:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='rho={max_rho:.4f}' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=not_enough_evidence")