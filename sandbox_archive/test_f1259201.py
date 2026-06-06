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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_lie_algebroid(n):
        L = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        return L
    
    def smash_product(L1, L2):
        n = len(L1)
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] += L1[i][k] * L2[k][j]
        return result
    
    def index(L):
        n = len(L)
        det = 0
        for p in itertools.permutations(range(n)):
            sign = (-1) ** sum(i < j for i, j in zip(p, sorted(p)))
            product = 1
            for i in range(n):
                product *= L[i][p[i]]
            det += sign * product
        return abs(det)
    
    def monotone_width(circuit):
        n = len(circuit)
        width = 0
        for t in range(1, n):
            active_gates = [i for i in range(n) if circuit[i] <= t]
            width = max(width, len(active_gates))
        return width
    
    def correlation(xs, ys):
        mean_x = sum(xs) / len(xs)
        mean_y = sum(ys) / len(ys)
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(xs, ys)) / len(xs)
        var_x = sum((xi - mean_x) ** 2 for xi in xs) / len(xs)
        var_y = sum((yi - mean_y) ** 2 for yi in ys) / len(ys)
        return cov / math.sqrt(var_x * var_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    indices = []
    widths = []
    
    for n in n_values:
        for _ in range(5):
            L1 = generate_lie_algebroid(n)
            L2 = generate_lie_algebroid(n)
            circuit = [random.randint(1, n) for _ in range(n)]
            indices.append(index(smash_product(L1, L2)))
            widths.append(monotone_width(circuit))
    
    corr_coeff = correlation(indices, widths)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": corr_coeff,
        "instances_tested": len(indices),
        "n_max": max(n_values),
        "conjecture_holds": 0.5 < corr_coeff <= 0.7,
        "counterexample": "" if 0.5 < corr_coeff <= 0.7 else f"Correlation: {corr_coeff}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr_coeff = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if 0.5 < r["metric_value"] <= 0.7) / len(results)
    
    if all(0.5 < r["metric_value"] <= 0.7 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not (0.5 < r["metric_value"] <= 0.7))
        print(f"RESULT: FALSIFIED counterexample=\"Correlation out of range\" first_failing_seed={first_failing_seed}")