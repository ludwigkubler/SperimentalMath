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
    
    def generate_boolean_function(n):
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def fourier_coefficients(f, n):
        N = 2**n
        a = [0] * N
        for k in range(N):
            sum_val = 0
            for x in range(N):
                sum_val += f[x] * math.cos(2 * math.pi * k * x / N)
            a[k] = sum_val / N
        return a
    
    def geometric_measure(a, n):
        norm_squared = sum(x**2 for x in a) / len(a)
        return norm_squared ** (0.5 * n)
    
    def communication_complexity_rank(f, n):
        M_f = [[f[(i >> j) & 1] for j in range(n)] for i in range(2**n)]
        rank = 0
        for i in range(len(M_f)):
            if any(M_f[i][j] != 0 for j in range(i, len(M_f))):
                rank += 1
                for j in range(i + 1, len(M_f)):
                    M_f[j][i] /= M_f[i][i]
                    for k in range(i + 1, len(M_f[0])):
                        M_f[j][k] -= M_f[j][i] * M_f[i][k]
        return rank
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)) / n)
        return cov / (std_x * std_y)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_boolean_function(n)
        a = fourier_coefficients(f, n)
        geo_measure = geometric_measure(a, n)
        rank = communication_complexity_rank(f, n)
        results.append((geo_measure, rank))
    
    x = [r[0] for r in results]
    y = [r[1] for r in results]
    correlation = pearson_correlation(x, y)
    
    return {
        "metric_name": "Pearson's Correlation Coefficient",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max([5, 10, 15, 20, 30, 40]),
        "conjecture_holds": correlation >= 0.7,
        "counterexample": "" if correlation >= 0.7 else "Pearson's Correlation Coefficient < 0.7"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='{result['counterexample']}' first_failing_seed={first_failing_seed}")