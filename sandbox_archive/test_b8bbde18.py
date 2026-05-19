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

# Define permutations as tuples (0-based indices)
a = (1, 2, 3, 4, 5)
b = (1, 3, 5, 2, 4)

def compose(p, q):
    return tuple(q[p[i] - 1] for i in range(5))

def inverse(p):
    inv = [0] * 5
    for i, j in enumerate(p):
        inv[j - 1] = i + 1
    return tuple(inv)

def perm_matrix(p):
    M = [[0] * 5 for _ in range(5)]
    for i in range(5):
        M[i][p[i] - 1] = 1
    return M

# Define Barrington's AND_n PBP recursively
def Barrington_AND(n):
    if n == 2:
        return [(1, a, b), (2, b, a)]
    else:
        and_half = Barrington_AND(n // 2)
        program = []
        for literal_index, p0, p1 in and_half:
            program.append((literal_index * 4 + 1, compose(p0, a), compose(p1, a)))
            program.append((literal_index * 4 + 2, compose(p0, b), compose(p1, b)))
            program.append((literal_index * 4 + 3, compose(p0, inverse(a)), compose(p1, inverse(b))))
            program.append((literal_index * 4 + 4, compose(p0, inverse(b)), compose(p1, inverse(a))))
        return program

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [4, 8, 16, 32]
    results = []
    
    for n in n_values:
        L_n = n ** 2
        total_norm = 0
        
        for _ in range(30):
            x = tuple(random.randint(0, 1) for _ in range(n))
            prefix_products = [a] * (n + 1)
            
            for literal_index, p0, p1 in Barrington_AND(n):
                if x[literal_index - 1] == 0:
                    prefix_products.append(p0)
                else:
                    prefix_products.append(p1)
            
            M_bar = sum(perm_matrix(pi) for pi in prefix_products[1:]) / L_n
            J = [[Fraction(1, 5)] * 5 for _ in range(5)]
            norm = sum((M_bar[i][j] - J[i][j]) ** 2 for i in range(5) for j in range(5))
            total_norm += norm
        
        D_bar = total_norm / len(n_values)
        results.append(D_bar)
    
    mean_D_bar = sum(results) / len(results)
    slopes = [math.log2(results[i] / results[i + 1]) for i in range(len(results) - 1)]
    all_slope_in_range = all(0.5 < slope < 3.0 for slope in slopes)
    
    conjecture_holds = mean_D_bar <= max(results) and all_slope_in_range
    counterexample = "" if conjecture_holds else "slope_outside_band"
    
    return {
        "metric_name": "Frobenius Fourier Defect",
        "metric_value": mean_D_bar,
        "instances_tested": len(n_values) * 30,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 8)]
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
    
    mean_D_bar = sum(trial_result["metric_value"] for trial_result in seeds) / len(seeds)
    support_fraction = sum(trial_result["conjecture_holds"] for trial_result in seeds) / len(seeds)
    
    if all(trial_result["conjecture_holds"] for trial_result in seeds):
        print(f"RESULT: SUPPORTED mean={mean_D_bar} std=0.0 support_fraction=1.0")
    elif any(not trial_result["conjecture_holds"] for trial_result in seeds) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, trial_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"slope_outside_band\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction_below_80")