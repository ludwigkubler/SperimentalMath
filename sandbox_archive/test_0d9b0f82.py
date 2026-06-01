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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tropicalize(boolean_function):
        n = len(boolean_function)
        tropical_matrix = [[-math.inf] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            tropical_matrix[i][i] = -math.inf
        for i in range(n):
            for j in range(i + 1, n):
                if boolean_function[2**i + 2**j]:
                    tropical_matrix[i][j] = 0
                    tropical_matrix[j][i] = 0
                else:
                    tropical_matrix[i][j] = math.inf
                    tropical_matrix[j][i] = math.inf
        return tropical_matrix
    
    def minimal_local_ring_unit_group_size(tropical_matrix):
        n = len(tropical_matrix) - 1
        unit_group_order = float('inf')
        for i in range(n):
            if tropical_matrix[i][n] == 0:
                unit_group_order = min(unit_group_order, 2)
        return unit_group_order
    
    def communication_complexity_rank(boolean_function):
        n = len(boolean_function)
        rank = 0
        for i in range(1, n + 1):
            if sum(boolean_function[j] for j in range(n) if (j & i) == i) > 0:
                rank += 1
        return rank
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y) if std_x * std_y != 0 else 0
    
    trials = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        boolean_function = generate_boolean_function(n)
        tropical_matrix = tropicalize(boolean_function)
        unit_group_size = minimal_local_ring_unit_group_size(tropical_matrix)
        rank = communication_complexity_rank(boolean_function)
        trials.append((unit_group_size, rank))
    
    if not trials:
        return {
            "metric_name": "Pearson Correlation",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    x, y = zip(*trials)
    correlation = pearson_correlation(x, y)
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": len(trials),
        "n_max": max(len(boolean_function) for _, boolean_function in trials),
        "conjecture_holds": 0.6 <= correlation < 0.8,
        "counterexample": "" if 0.6 <= correlation < 0.8 else f"Correlation {correlation:.2f} outside [0.6, 0.8)"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction}")
    elif any("conjecture_holds" in r and not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "conjecture_holds" in result and not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation outside [0.6, 0.8)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds tested")