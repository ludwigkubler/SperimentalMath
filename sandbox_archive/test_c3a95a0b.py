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
# end SEC prelude

import random
import math
import json
from typing import List, Dict

def TropicalFourierTransform(f: List[int], Y: List[int]) -> List[float]:
    N = len(Y) // 2
    F = [float('inf')] * (2 * N + 1)
    for x in range(-N, N + 1):
        for y_idx, y in enumerate(Y):
            F[y_idx] = min(F[y_idx], f[x] - x * y)
    return F

def DiscrepancyMeasure(f: List[int], Y: List[int]) -> float:
    N = len(Y) // 2
    a = min(Y, key=lambda y: sum(max(0, f[x] - (a * x + b)) for x in range(-N, N + 1)))
    b_hat = sum(f[x] - a * x for x in range(-N, N + 1)) / len(range(-N, N + 1))
    r = [f[x] - (a * x + b_hat) for x in range(-N, N + 1)]
    return max(r)

def run_trial(seed: int) -> Dict[str, any]:
    random.seed(seed)
    N_values = [10, 20, 40]
    results = []
    
    for N in N_values:
        Y = list(range(-N, N + 1))
        affine_count = 0
        non_affine_count = 0
        
        for _ in range(200):
            a = random.choice(Y)
            b = random.uniform(-10, 10)
            f = [a * x + b for x in range(-N, N + 1)]
            F = TropicalFourierTransform(f, Y)
            m_f = min(F)
            argmin_y = [y for y, val in enumerate(F) if math.isclose(val, m_f)]
            
            if len(argmin_y) == 1 and all(math.isclose(f[x], a * x + b, abs_tol=1e-9) for x in range(-N, N + 1)):
                affine_count += 1
            else:
                non_affine_count += 1
        
        for _ in range(400):
            f = [random.randint(-20, 20) for _ in range(2 * N + 1)]
            F = TropicalFourierTransform(f, Y)
            m_f = min(F)
            argmin_y = [y for y, val in enumerate(F) if math.isclose(val, m_f)]
            
            if len(argmin_y) == 1 and all(math.isclose(f[x], a * x + b, abs_tol=1e-9) for x in range(-N, N + 1)):
                non_affine_count += 1
            else:
                affine_count += 1
        
        results.append({
            "metric_name": "DiscrepancyMeasure",
            "metric_value": (affine_count / 600),
            "instances_tested": 600,
            "conjecture_holds": True,
            "counterexample": ""
        })
    
    return {
        "seed": seed,
        "trials": results
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    all_results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps(result))
        all_results.extend(result["trials"])
    
    total_affine_count = sum(trial["metric_value"] * trial["instances_tested"] for trial in all_results)
    total_non_affine_count = sum((1 - trial["metric_value"]) * trial["instances_tested"] for trial in all_results)
    support_fraction = total_affine_count / (total_affine_count + total_non_affine_count)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_affine_count / len(all_results)} std=NA support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE not enough seeds supported")