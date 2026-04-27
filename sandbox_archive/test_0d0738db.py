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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def max_element(lst):
    return max(lst)

def min_element(lst):
    return min(lst)

def mean(lst):
    return sum(lst) / len(lst)

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        # Find the pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        
        # Eliminate the pivot column
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    
    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def tropical_polynomial_eval(f, x):
    return max(a * x + b for a, b in f)

def tropical_fourier_transform(f, y):
    d = len(y)
    grid_size = 41
    F = [0] * (grid_size ** d)
    for i in range(grid_size ** d):
        x = [i // (grid_size ** j) % grid_size - 20.5 for j in range(d)]
        F[i] = y[i] * tropical_polynomial_eval(f, x)
    return F

def discrepancy_calculation(f):
    d = len(next(iter(f)))
    grid_size = 41
    total = 0
    count = 0
    for i in range(grid_size ** d):
        x = [i // (grid_size ** j) % grid_size - 20.5 for j in range(d)]
        total += f(x)
        count += 1
    mean_val = total / count
    return max(f(x) for x in product(range(-20, 21), repeat=d)) - mean_val

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    d = random.choice([1, 2])
    n = random.randint(3, 8)
    f = [(random.uniform(-10, 10), random.uniform(-10, 10)) for _ in range(n)]
    
    MFC_f = min(tropical_fourier_transform(f, [y for y in range(-20, 21)]))
    Disc_f = discrepancy_calculation(f)
    
    lambda_values = [random.uniform(0.1, 5) for _ in range(10)]
    results = []
    for λ in lambda_values:
        g = [(λ * a, b) for a, b in f]
        MFC_g = min(tropical_fourier_transform(g, [y for y in range(-20, 21)]))
        Disc_g = discrepancy_calculation(g)
        
        slack_f = max(abs(tropical_fourier_transform(f, [y for y in range(-20, 21)])[i]) - Disc_f for i in range(len(tropical_fourier_transform(f, [y for y in range(-20, 21)]))))
        slack_g = max(abs(tropical_fourier_transform(g, [y for y in range(-20, 21)])[i]) - Disc_g for i in range(len(tropical_fourier_transform(g, [y for y in range(-20, 21)]))))
        
        results.append({
            "lambda": λ,
            "MFC_f": MFC_f,
            "MFC_g": MFC_g,
            "Disc_f": Disc_f,
            "Disc_g": Disc_g,
            "slack_f": slack_f,
            "slack_g": slack_g
        })
    
    conjecture_holds = all(abs(result["MFC_g"] - result["lambda"] * result["MFC_f"]) < 1e-9 and abs(result["Disc_g"] - result["lambda"] * result["Disc_f"]) < 1e-9 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "MFC and Discrepancy",
        "metric_value": mean([result["MFC_g"] - result["lambda"] * result["MFC_f"] for result in results]),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = mean([r["metric_value"] for r in results])
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")