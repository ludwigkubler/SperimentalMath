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

def TropicalFourierTransform(f, Y):
    N = len(Y) // 2
    F = [float('inf')] * (N + 1)
    for x in range(-N, N + 1):
        for y_idx, y in enumerate(Y):
            F[y_idx] = min(F[y_idx], f(x) - x * y)
    return F

def DiscrepancyMeasure(f, Y):
    N = len(Y) // 2
    max_f = max(f(x) for x in range(-N, N + 1))
    min_f = min(f(x) for x in range(-N, N + 1))
    a_hat = min(Y, key=lambda y: sum(abs(f(x) - (a * x + b)) for x in range(-N, N + 1)))
    b_hat = f(0) - a_hat * 0
    r = [f(x) - (a_hat * x - b_hat) for x in range(-N, N + 1)]
    Disc = max(r)
    return Disc

def run_trial(seed: int) -> dict:
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
            f = lambda x: a * x + b
            F = TropicalFourierTransform(f, Y)
            m_f = min(F)
            argmin_F = [y for y in Y if F[Y.index(y)] == m_f]
            Disc = DiscrepancyMeasure(f, Y)
            
            if len(argmin_F) == 1 and all(abs(f(x) - (a * x + b)) < 1e-9 for x in range(-N, N + 1)):
                affine_count += 1
            else:
                non_affine_count += 1
        
        for _ in range(400):
            f = lambda x: random.randint(-20, 20)
            F = TropicalFourierTransform(f, Y)
            m_f = min(F)
            argmin_F = [y for y in Y if F[Y.index(y)] == m_f]
            Disc = DiscrepancyMeasure(f, Y)
            
            if len(argmin_F) != 1 or not all(abs(f(x) - (a * x + b)) < 1e-9 for x in range(-N, N + 1)):
                non_affine_count += 1
            else:
                affine_count += 1
        
        results.append({
            "metric_name": "DiscrepancyMeasure",
            "metric_value": Disc,
            "instances_tested": 600,
            "conjecture_holds": len(argmin_F) == 1 and all(abs(f(x) - (a * x + b)) < 1e-9 for x in range(-N, N + 1)),
            "counterexample": ""
        })
    
    mean_disc = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_disc": mean_disc,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": result}))
        results.append(result)
    
    mean_disc = sum(result["mean_disc"] for result in results) / len(results)
    support_fraction = sum(result["support_fraction"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_disc} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")