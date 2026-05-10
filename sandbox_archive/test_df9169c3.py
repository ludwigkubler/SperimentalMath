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
# end SEC prelude

import random
import math
from typing import List, Dict

def generate_read_once_bp(n: int) -> List[List[int]]:
    bp = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    return bp

def generate_read_twice_bp(n: int) -> List[List[List[int]]]:
    bp = [[[random.randint(0, 1) for _ in range(n)] for _ in range(n)] for _ in range(n)]
    return bp

def discrete_fourier_transform(bp: List[List[int]]) -> List[List[complex]]:
    n = len(bp)
    omega = [math.exp(-2j * math.pi * i / n) for i in range(n)]
    F = [[0] * n for _ in range(n)]
    for k in range(n):
        for l in range(n):
            sum_val = 0
            for i in range(n):
                sum_val += bp[i][k] * omega[(i * l) % n]
            F[k][l] = sum_val / math.sqrt(n)
    return F

def non_commutative_fourier_norm(F: List[List[complex]]) -> float:
    norm = 0
    for row in F:
        for val in row:
            norm += abs(val)
    return norm

def run_trial(seed: int) -> Dict[str, any]:
    random.seed(seed)
    n = 40
    read_once_bp = generate_read_once_bp(n)
    read_twice_bp = generate_read_twice_bp(n)
    
    F_ro = discrete_fourier_transform(read_once_bp)
    F_rt = discrete_fourier_transform(read_twice_bp)
    
    norm_ro = non_commutative_fourier_norm(F_ro)
    norm_rt = non_commutative_fourier_norm(F_rt)
    
    metric_name = "non_commutative_fourier_norm"
    metric_value_ro = norm_ro
    metric_value_rt = norm_rt
    
    instances_tested = 2
    conjecture_holds = (norm_rt >= n / 2) and (norm_ro <= math.log(n))
    counterexample = "" if conjecture_holds else "read_once_bp" if norm_ro > n / 2 else "read_twice_bp"
    
    return {
        "metric_name": metric_name,
        "metric_value_ro": metric_value_ro,
        "metric_value_rt": metric_value_rt,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ro = sum(r["metric_value_ro"] for r in results) / len(results)
    std_ro = math.sqrt(sum((r["metric_value_ro"] - mean_ro)**2 for r in results) / len(results))
    mean_rt = sum(r["metric_value_rt"] for r in results) / len(results)
    std_rt = math.sqrt(sum((r["metric_value_rt"] - mean_rt)**2 for r in results) / len(results))
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean_ro={mean_ro} std_ro={std_ro} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"read_once_bp\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")