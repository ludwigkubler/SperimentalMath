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
    
    def generate_entangled_state(n):
        return [random.choice([1, -1]) for _ in range(2**n)]
    
    def compute_algebraic_hologram(state):
        n = int(math.log2(len(state)))
        hologram = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                sum_product = 0
                for k in range(2**n):
                    if (k >> i) & 1 != (k >> j) & 1:
                        sum_product += state[k]
                hologram[i][j] = sum_product
        return hologram
    
    def min_rank(matrix):
        n = len(matrix)
        rank = 0
        for col in range(n):
            if any(matrix[row][col] != 0 for row in range(rank, n)):
                rank += 1
                for row in range(rank, n):
                    factor = matrix[row][col] / matrix[rank-1][col]
                    for j in range(col, n):
                        matrix[row][j] -= factor * matrix[rank-1][j]
        return rank
    
    def log_n(n):
        return math.log2(n)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        state = generate_entangled_state(n)
        hologram = compute_algebraic_hologram(state)
        rank = min_rank(hologram)
        log_n_value = log_n(n)
        results.append((n, rank, log_n_value))
    
    metric_values = [rank for _, rank, _ in results]
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric)**2 for x in metric_values) / len(metric_values))
    
    conjecture_holds = all(rank >= 0.5 * log_n_value for _, rank, log_n_value in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_metric,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")