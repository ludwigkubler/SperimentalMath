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

def generate_symmetric_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def symmetric_polynomial_representation(f):
    n = int(math.log2(len(f)))
    poly = [[f[i] if i & (1 << j) else f[i ^ (1 << j)] for j in range(n)] for i in range(len(f))]
    return poly

def gram_matrix(poly):
    n = len(poly)
    G = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            sum_val = 0
            for k in range(n):
                sum_val += poly[i][k] * poly[j][k]
            G[i][j] = sum_val
            G[j][i] = sum_val
    return G

def eigenvalues(G):
    n = len(G)
    if n == 1:
        return [G[0][0]]
    
    def det(A, k):
        if k == 2:
            return A[0][0] * A[1][1] - A[0][1] * A[1][0]
        det_val = 0
        for c in range(k):
            submatrix = [row[:c] + row[c+1:] for row in A[1:]]
            sign = (-1) ** (c % 2)
            sub_det = det(submatrix, k-1)
            det_val += sign * A[0][c] * sub_det
        return det_val
    
    eigenvals = []
    for i in range(n):
        G_copy = [row[:] for row in G]
        for j in range(i+1, n):
            G_copy[j][i] /= G[i][i]
        for j in range(i+1, n):
            for k in range(i+1, n):
                G_copy[j][k] -= G_copy[j][i] * G_copy[i][k]
        eigenvals.append(G_copy[0][0])
    return eigenvals

def abp_width(f):
    n = int(math.log2(len(f)))
    dp = [[float('inf')] * (n+1) for _ in range(1 << n)]
    dp[0][0] = 0
    for i in range(1, 1 << n):
        for j in range(n):
            if i & (1 << j):
                dp[i][j+1] = min(dp[i][j+1], dp[i ^ (1 << j)][j] + 1)
    return dp[(1 << n) - 1][n]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_symmetric_boolean_function(n)
        poly = symmetric_polynomial_representation(f)
        G = gram_matrix(poly)
        eigenvals = eigenvalues(G)
        rank = len(eigenvals)
        
        width = abp_width(f)
        if width == float('inf'):
            return {
                "metric_name": "rank*width",
                "metric_value": None,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        results.append((n, rank * width))
    
    mean = sum(x[1] for x in results) / len(results)
    std_dev = math.sqrt(sum((x[1] - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for _, value in results if abs(value - n_values[0]) < 1e-6) / len(results)
    
    return {
        "metric_name": "rank*width",
        "metric_value": mean,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"n={results[0][0]}, rank*width={results[0][1]}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
    
    results = [run_trial(seed) for seed in seeds]
    mean = sum(x['metric_value'] for x in results if x['metric_value'] is not None) / len(results)
    std_dev = math.sqrt(sum((x['metric_value'] - mean) ** 2 for x in results if x['metric_value'] is not None) / len(results))
    support_fraction = sum(1 for result in results if abs(result['metric_value'] - n_values[0]) < 1e-6) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(result['counterexample']):
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={seeds[results.index(result)]}")
    else:
        print(f"RESULT: INCONCLUSIVE no valid data")