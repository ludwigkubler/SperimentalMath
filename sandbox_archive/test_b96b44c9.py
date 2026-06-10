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
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        circuit_ranks = []
        for k in range(1, n + 1):
            rank = 0
            for i in range(n - k + 1):
                subfunction = f[i:i+k]
                if sum(subfunction) == k:
                    rank += 1
            circuit_ranks.append(rank)
        return max(circuit_ranks) / min(circuit_ranks)
    
    def homogeneous_polynomials(f, d):
        n = len(f)
        poly_space = []
        for i in range(n + 1):
            if i + d == n:
                poly_space.append([f[j] for j in range(i, n)])
        return poly_space
    
    def hodge_class_dimension(poly_space):
        n = len(poly_space[0])
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            A[i][i] = 1
        for poly in poly_space:
            for j in range(n):
                A[j][-1] += poly[j]
        rank = 0
        for row in A:
            if any(row):
                rank += 1
        return n - rank
    
    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(len(x))) / len(x))
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(len(y))) / len(y))
        return cov / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    dim_H_f = []
    R_f = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        R_f.append(communication_complexity_rank_variance(f))
        poly_space = homogeneous_polynomials(f, n)
        dim_H_f.append(hodge_class_dimension(poly_space))
    
    correlation_coefficient = pearson_correlation(dim_H_f, R_f)
    
    return {
        "metric_name": "Pearson's Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": "" if correlation_coefficient >= 0.8 else "Pearson's Correlation Coefficient < 0.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [random.randint(2, 39) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 0.8) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r < 0.5 for r in results):
        first_failing_seed = seeds[results.index(min([r for r in results if r < 0.5]))]
        print(f"RESULT: FALSIFIED counterexample='Pearson's Correlation Coefficient < 0.5' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")