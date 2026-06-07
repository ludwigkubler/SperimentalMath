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
    
    def generate_protocol(n):
        # Generate a random n-ary communication protocol
        return [random.randint(1, n) for _ in range(random.randint(5, 10))]
    
    def information_matrix(protocol):
        # Compute the information matrix for the given protocol
        n = len(set(protocol))
        I = [[0] * n for _ in range(n)]
        for x in protocol:
            I[x-1][x-1] += 1
        return I
    
    def rank_variance(matrix):
        # Compute the rank variance of the matrix
        det = determinant(matrix)
        if det == 0:
            return float('inf')
        rank = len([i for i, row in enumerate(matrix) if any(row[j] != 0 for j in range(len(row)))])
        return (rank - n / len(matrix)) ** 2
    
    def determinant(matrix):
        # Compute the determinant of a square matrix using Gaussian elimination
        n = len(matrix)
        A = [row[:] for row in matrix]
        det = 1
        for i in range(n):
            if A[i][i] == 0:
                for j in range(i+1, n):
                    if A[j][i] != 0:
                        A[i], A[j] = A[j], A[i]
                        det *= -1
                        break
                else:
                    return 0
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return det
    
    def minimal_order(matrix):
        # Compute the minimal order of local units in the adjoint group
        n = len(matrix)
        G = set()
        for i in range(n):
            for j in range(i+1, n):
                if matrix[i][j] != 0:
                    G.add((i, j))
        return len(G)
    
    def pearson_correlation(x, y):
        # Compute the Pearson correlation coefficient
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov / (std_x * std_y)
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        for _ in range(5):
            protocol = generate_protocol(n)
            I = information_matrix(protocol)
            rank_var = rank_variance(I)
            order = minimal_order(I)
            results.append((order, rank_var))
    
    if len(results) < 30 * len(n_values):
        return {
            "metric_name": "Pearson Correlation",
            "metric_value": float('nan'),
            "instances_tested": len(results),
            "n_max": max(len(set(protocol)) for protocol in [generate_protocol(n) for n in n_values]),
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    orders, rank_vars = zip(*results)
    corr = pearson_correlation(orders, rank_vars)
    mean_rank_var = sum(rank_vars) / len(rank_vars)
    std_rank_var = math.sqrt(sum((x - mean_rank_var) ** 2 for x in rank_vars) / len(rank_vars))
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": corr,
        "instances_tested": len(results),
        "n_max": max(len(set(protocol)) for protocol in [generate_protocol(n) for n in n_values]),
        "conjecture_holds": corr >= 0.8 and mean_rank_var > 0 and std_rank_var > 0,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    std_corr = math.sqrt(sum((r["metric_value"] - mean_corr) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")