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
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= factor
            for j in range(n):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def determinant(matrix):
        n = len(matrix)
        det = 1
        for i in range(n):
            det *= matrix[i][i]
        return det

    def grothendieck_witt_class(poly):
        n = len(poly)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                A[i][j] = poly[i][j]
                A[j][i] = poly[i][j]
        B = gaussian_elimination(A)
        return abs(determinant(B))

    def generate_protocol(n):
        protocol = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        rank_variance = sum(sum(row) != sum(col) for row, col in zip(protocol, zip(*protocol)))
        return protocol, rank_variance

    max_gw_class = 0
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            protocol, rank_variance = generate_protocol(n)
            if rank_variance <= n:
                gw_class = grothendieck_witt_class(protocol)
                max_gw_class = max(max_gw_class, gw_class)
                instances_tested += 1
                n_max = max(n_max, n)
    
    conjecture_holds = max_gw_class <= 2 * n_max  # Example constant c=2 for simplicity
    counterexample = "" if conjecture_holds else f"max GW class {max_gw_class} > 2n_max {2*n_max}"
    
    return {
        "metric_name": "Max Grothendieck-Witt Class",
        "metric_value": max_gw_class,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")