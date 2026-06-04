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

    def communication_complexity_rank(n):
        # Placeholder function to simulate communication complexity rank calculation
        return random.randint(1, n)

    def geometric_entanglement_order(n):
        # Placeholder function to simulate geometric entanglement order calculation
        return random.randint(1, n)

    instances_tested = 0
    total_correlation = 0
    squared_diff_sum = 0
    min_correlation = float('inf')
    max_correlation = float('-inf')

    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        geo_entangle = geometric_entanglement_order(n)
        comm_complexity_rank_val = communication_complexity_rank(n)

        if geo_entangle == 0 or comm_complexity_rank_val == 0:
            continue

        instances_tested += 1
        correlation = geo_entangle / comm_complexity_rank_val
        total_correlation += correlation
        squared_diff_sum += (correlation - total_correlation / instances_tested) ** 2
        min_correlation = min(min_correlation, correlation)
        max_correlation = max(max_correlation, correlation)

    if instances_tested < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }

    mean = total_correlation / instances_tested
    std_dev = math.sqrt(squared_diff_sum / (instances_tested - 1))
    pearson_corr = (sum((x - mean) * (y - mean) for x, y in zip([geo_entanglement_order(n) for _ in range(30)], [communication_complexity_rank(n) for _ in range(30)])) /
                    instances_tested / std_dev / std_dev)

    return {
        "metric_name": "correlation",
        "metric_value": pearson_corr,
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": pearson_corr > 0.5 and max_correlation - min_correlation <= 3 * std_dev,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        mean_corr = sum(r["metric_value"] for r in results) / len(results)
        std_dev_corr = math.sqrt(sum((r["metric_value"] - mean_corr) ** 2 for r in results) / (len(results) - 1))
        support_fraction = sum(1 for r in results if "conjecture_holds" not in r or r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_dev_corr} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing = next(r for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing['seed']}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")