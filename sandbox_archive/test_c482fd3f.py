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
    
    def gaussian_elimination(matrix, mod):
        n = len(matrix)
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            pivot = matrix[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                if j != i:
                    factor = (matrix[j][i] * pow(pivot, -1, mod)) % mod
                    for k in range(n + 1):
                        matrix[j][k] = (matrix[j][k] - factor * matrix[i][k]) % mod
            matrix[i][i] = 1
        return matrix
    
    def rank(matrix, mod):
        n = len(matrix)
        row_echelon_form = gaussian_elimination(matrix, mod)
        rank = sum(1 for row in row_echelon_form if any(row[j] != 0 for j in range(n)))
        return rank
    
    def communication_complexity_rank_variance(rank_values):
        mean = sum(rank_values) / len(rank_values)
        variance = sum((x - mean) ** 2 for x in rank_values) / len(rank_values)
        return variance
    
    def noncommutative_yang_baxter_order(n, mod):
        # Placeholder function to simulate NCYBE order calculation
        # This is a dummy implementation and should be replaced with actual logic
        return n * (n + 1) // 2
    
    n_min = 5
    n_max = 40
    instances_tested = 30
    rank_values = []
    
    for _ in range(instances_tested):
        n = random.randint(n_min, n_max)
        matrix = [[random.randint(0, mod - 1) for _ in range(n)] for _ in range(n)]
        rank_value = rank(matrix, mod)
        rank_values.append(rank_value)
    
    nc_yang_baxter_order = noncommutative_yang_baxter_order(n_max, 2 ** 31 - 1)
    rank_variance = communication_complexity_rank_variance(rank_values)
    
    correlation_coefficient = (len(rank_values) * sum(x * y for x, y in zip(nc_yang_baxter_order, rank_values)) -
                               sum(nc_yang_baxter_order) * sum(rank_values)) / \
                              math.sqrt((len(rank_values) * sum(x ** 2 for x in nc_yang_baxter_order) - sum(nc_yang_baxter_order) ** 2) *
                                        (len(rank_values) * sum(y ** 2 for y in rank_values) - sum(rank_values) ** 2))
    
    conjecture_holds = correlation_coefficient >= 0.75
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")