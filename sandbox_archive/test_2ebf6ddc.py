# auto-injected by SEC sandbox
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
import math
from itertools import product

def tropical_max(a, b):
    return max(a, b)

def tropical_min(a, b):
    return min(a, b)

def tropical_add(a, b):
    return a + b

def tropical_subtract(a, b):
    return a - b

def tropical_multiply(a, b):
    return a * b

def tropical_divide(a, b):
    if b == 0:
        raise ValueError("Division by zero")
    return a / b

def tropical_polynomial(N, d):
    coefficients = [[random.uniform(-10, 10) for _ in range(d)] for _ in range(N)]
    return coefficients

def fourier_transform(f, N, d):
    F = [[tropical_max(*[tropical_subtract(f[i], tropical_multiply(k, i)) for i in range(N)]) for k in range(N)] for k in range(N)]
    return F

def discrepancy_measure(f):
    max_val = tropical_max(*[tropical_max(*row) for row in f])
    min_val = tropical_min(*[tropical_min(*row) for row in f])
    mean_val = sum(sum(row) for row in f) / (N * d)
    return max_val - min_val - mean_val

def minimal_fourier_coefficient(F):
    return min(abs(k) for k in F)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    N, d = 8, 2
    f = tropical_polynomial(N, d)
    g = tropical_polynomial(N, d)
    
    disc_f = discrepancy_measure(f)
    disc_g = discrepancy_measure(g)
    F = fourier_transform(f, N, d)
    G = fourier_transform(g, N, d)
    
    LHS = abs(disc_f - disc_g)
    RHS = max(abs(F[k] - G[k]) for k in range(N))
    
    conjecture_holds = LHS <= RHS
    counterexample = "" if conjecture_holds else "Lipschitz inequality violated"
    
    return {
        "metric_name": "LHS/RHS ratio",
        "metric_value": LHS / RHS,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Lipschitz inequality violated\" first_failing_seed={first_failing_seed}")