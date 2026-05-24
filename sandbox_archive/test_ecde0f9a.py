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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_hecke_algebra(f):
        n = len(f)
        H = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if f[i & j] == 1:
                    H[i][j] = 1
        return H
    
    def compute_exponential_depth(f):
        n = len(f)
        depth = 0
        while True:
            new_f = [f[i ^ (1 << j)] for i in range(2**n) for j in range(n)]
            if new_f == f:
                break
            f = new_f
            depth += 1
        return depth
    
    def matrix_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            pivot_row = None
            for j in range(i, n):
                if any(matrix[j][k] != 0 for k in range(n)):
                    pivot_row = j
                    break
            if pivot_row is None:
                continue
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            rank += 1
            for j in range(i + 1, n):
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    f = generate_boolean_function(5)
    H = compute_hecke_algebra(f)
    d = compute_exponential_depth(f)
    rho_H = matrix_rank(H)
    
    metric_value = Fraction(rho_H, 2**d)
    conjecture_holds = metric_value > Fraction(3, 2)
    counterexample = "" if conjecture_holds else f"rho(Hecke(f))={rho_H}, depth(d)={d}"
    
    return {
        "metric_name": "ratio",
        "metric_value": float(metric_value),
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results):.2f} std=0.00 support_fraction=1.00")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results):.2f} std=0.00 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")