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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def information_matrix(protocol):
        n = len(protocol)
        I = [[0] * n for _ in range(n)]
        for x, y in protocol:
            if 1 <= x <= n and 1 <= y <= n:
                I[x-1][y-1] += 1
        return I
    
    def rank_variance(matrix):
        n = len(matrix)
        det = determinant(matrix)
        if det == 0:
            return float('inf')
        trace = sum(matrix[i][i] for i in range(n))
        return (trace**2 - sum(matrix[i][j]**2 for i in range(n) for j in range(i+1, n))) / (n * det**2)
    
    def determinant(matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        det = 0
        for c in range(len(matrix)):
            submatrix = [row[:c] + row[c+1:] for row in matrix[1:]]
            det += ((-1)**c) * matrix[0][c] * determinant(submatrix)
        return det
    
    def minimal_order_of_local_units(matrix):
        n = len(matrix)
        G = []
        for i in range(n):
            for j in range(i+1, n):
                if matrix[i][j] != 0:
                    G.append((i, j))
        return len(G)
    
    def generate_protocol(n):
        protocol = set()
        while len(protocol) < n**2 - n:
            x = random.randint(1, n)
            y = random.randint(1, n)
            if (x, y) not in protocol and (y, x) not in protocol:
                protocol.add((x, y))
        return list(protocol)
    
    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        std_x = math.sqrt(sum((xi - mean_x)**2 for xi in x) / len(x))
        std_y = math.sqrt(sum((yi - mean_y)**2 for yi in y) / len(y))
        return cov / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        protocol = generate_protocol(n)
        I = information_matrix(protocol)
        rank_variances = [rank_variance(I) for _ in range(30)]
        min_orders = [minimal_order_of_local_units(I) for _ in range(30)]
        correlation = pearson_correlation(min_orders, rank_variances)
        results.append({
            "n": n,
            "correlation": correlation,
            "min_orders": min_orders,
            "rank_variances": rank_variances
        })
    
    mean_corr = sum(result["correlation"] for result in results) / len(results)
    std_corr = math.sqrt(sum((result["correlation"] - mean_corr)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if abs(result["correlation"]) >= 0.8) / len(results)
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": mean_corr,
        "instances_tested": sum(len(result["min_orders"]) for result in results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else "Pearson correlation < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(result["metric_value"] for result in results) / len(results)
    std_corr = math.sqrt(sum((result["metric_value"] - mean_corr)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if abs(result["metric_value"]) >= 0.8) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif any(abs(result["metric_value"]) < 0.8 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"]) < 0.8)
        print(f"RESULT: FALSIFIED counterexample='Pearson correlation < 0.8' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")