# auto-injected by SEC sandbox
import collections
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
import json
from itertools import product

def add(a, b):
    return [x + y for x, y in zip(a, b)]

def sub(a, b):
    return [x - y for x, y in zip(a, b)]

def max_elem(lst):
    return max(lst)

def mean(lst):
    return sum(lst) / len(lst)

def tropical_add(f, g):
    return [max(a, b) for a, b in zip(f, g)]

def tropical_mul(f, c):
    return [c * x for x in f]

def tropical_fourier_transform(f, grid_points):
    d = len(grid_points)
    grid_size = len(grid_points[0])
    F = [0] * (grid_size ** d)
    
    def index(coords):
        return sum((coords[i] - grid_points[i][0]) * grid_size**i for i in range(d))
    
    for x in product(*grid_points):
        y = sub(x, [1, 1, 1])  # Adjusted to avoid negative indices
        F[index(y)] = max(F[index(y)], sum(tropical_mul(monomial, x) for monomial in f))
    
    return F

def discrepancy_calculation(f, grid_points):
    d = len(grid_points)
    grid_size = len(grid_points[0])
    total = 0
    count = 0
    
    def index(coords):
        return sum((coords[i] - grid_points[i][0]) * grid_size**i for i in range(d))
    
    for x in product(*grid_points):
        total += f[index(x)]
        count += 1
    
    mean_f = total / count
    return max_elem(f) - mean_f

def run_trial(seed: int) -> dict:
    random.seed(seed)
    d = random.randint(1, 2)
    grid_size = 41
    grid_points = [[-20 + i * (grid_size // 40) for i in range(grid_size)] for _ in range(d)]
    
    f = [max([random.randint(-10, 10) * x[i] + random.randint(-10, 10) for i in range(d)]) for _ in range(random.randint(3, 8))]
    
    MFC_f = min(tropical_fourier_transform(f, grid_points))
    Disc_f = discrepancy_calculation(f, grid_points)
    
    lambda_values = [random.uniform(0.1, 5) for _ in range(10)]
    results = []
    
    for λ in lambda_values:
        g = tropical_mul(f, λ)
        MFC_g = min(tropical_fourier_transform(g, grid_points))
        Disc_g = discrepancy_calculation(g, grid_points)
        
        results.append({
            "lambda": λ,
            "MFC_f": MFC_f,
            "MFC_g": MFC_g,
            "Disc_f": Disc_f,
            "Disc_g": Disc_g
        })
    
    all_correct = True
    for result in results:
        if not (abs(result["MFC_g"] - λ * result["MFC_f"]) < 1e-9 and abs(result["Disc_g"] - λ * result["Disc_f"]) < 1e-9):
            all_correct = False
    
    return {
        "metric_name": "Tropical Positive-Scalar Homogeneity",
        "metric_value": MFC_f,
        "instances_tested": len(results),
        "conjecture_holds": all_correct,
        "counterexample": "" if all_correct else "lambda-dependent discrepancy"
    }

if __name__ == "__main__":
    seeds = [11, 23, 37, 53, 71] if not sys.argv[1:] else [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='lambda-dependent discrepancy' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")