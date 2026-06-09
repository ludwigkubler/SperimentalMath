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
    
    def generate_circuit(n, d):
        if n == 1:
            return [random.choice([0, 1])]
        else:
            left = generate_circuit(n // 2, d - 1)
            right = generate_circuit(n - n // 2, d - 1)
            return [left[i] and right[i] for i in range(len(left))] + [left[i] or right[i] for i in range(len(right))]
    
    def compute_hausdorff_dimension(output_set):
        # Simplified approximation of Hausdorff dimension
        n = len(output_set)
        if n == 0:
            return 0
        min_distance = float('inf')
        max_distance = 0
        for i in range(n):
            for j in range(i + 1, n):
                distance = abs(output_set[i] - output_set[j])
                if distance < min_distance:
                    min_distance = distance
                if distance > max_distance:
                    max_distance = distance
        return math.log(max_distance / min_distance) / math.log(n)
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        covariance = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        std_dev_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_dev_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return covariance / (std_dev_x * std_dev_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        circuit = generate_circuit(n, d=10)
        output_set = set(circuit)
        hausdorff_dim = compute_hausdorff_dimension(output_set)
        expected = n ** (1 / 10)
        results.append((n, hausdorff_dim, expected))
    
    correlation = correlation_coefficient([r[1] for r in results], [r[2] for r in results])
    conjecture_holds = correlation >= 0.8
    counterexample = "" if conjecture_holds else "correlation < 0.8"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")