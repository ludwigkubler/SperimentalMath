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
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = max(range(i, rows), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = 1 / matrix[i][i]
            for j in range(cols):
                matrix[i][j] *= factor
            for k in range(rows):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(cols):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix

    def min_rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for i in range(min(rows, cols)):
            if any(matrix[j][i] != 0 for j in range(i, rows)):
                rank += 1
        return rank

    def k_clique_instance(n, k):
        vertices = list(range(n))
        edges = []
        for _ in range(k * (k - 1) // 2):
            u, v = random.sample(vertices, 2)
            if u > v:
                u, v = v, u
            edges.append((u, v))
        return edges

    def twisted_group_algebra(edges):
        # Simplified representation for demonstration purposes
        n = len(edges) + 1
        algebra = [[0] * n for _ in range(n)]
        for i in range(n):
            algebra[i][i] = 1
        for u, v in edges:
            algebra[u][v] = algebra[v][u] = -1
        return gaussian_elimination(algebra)

    def monotone_circuit_depth(k):
        # Simplified estimation using known bounds
        return k * math.log2(k)

    n = random.choice([5, 10, 15, 20, 30, 40])
    k = random.randint(2, min(n - 1, 5))
    instance = k_clique_instance(n, k)
    algebra = twisted_group_algebra(instance)
    rank = min_rank(algebra)
    depth = monotone_circuit_depth(k)

    ratio = rank / (2 ** (n - k) * k)
    conjecture_holds = ratio >= 0.5 and ratio < 0.3
    counterexample = "" if conjecture_holds else f"Ratio {ratio} outside [0.5, 0.3]"

    return {
        "metric_name": "Ratio of Minimal Rank to Bound",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.3 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0.3)
        print(f"RESULT: FALSIFIED counterexample=\"Ratio outside [0.5, 0.3]\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")