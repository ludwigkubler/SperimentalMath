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
    
    def generate_circuit(n):
        if n == 1:
            return [random.choice([0, 1])]
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - n // 2)
            return [random.choice([0, 1]) for _ in range(n)] + left + right
    
    def compute_local_ring(circuit):
        n = len(circuit)
        ring = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            ring[i][i] = 1
        for i in range(n):
            if circuit[i] == 1:
                for j in range(i, n + 1):
                    ring[j][j - 1] += ring[j][i]
                    ring[j][i] -= ring[j][i - 1]
        return ring
    
    def measure_unit_group_size(ring):
        n = len(ring) - 1
        unit_group_size = 0
        for i in range(n + 1):
            if all(ring[i][j] == 0 for j in range(i, n + 1)):
                unit_group_size += 1
        return unit_group_size
    
    def measure_monotone_width(circuit):
        n = len(circuit)
        width = 0
        for i in range(n):
            if circuit[i] == 1:
                width += 1
        return width
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        if std_x == 0 or std_y == 0:
            return 0
        return cov_xy / (std_x * std_y)
    
    unit_group_sizes = []
    monotone_widths = []
    
    for _ in range(100):
        circuit = generate_circuit(random.randint(5, 40))
        ring = compute_local_ring(circuit)
        unit_group_size = measure_unit_group_size(ring)
        monotone_width = measure_monotone_width(circuit)
        unit_group_sizes.append(unit_group_size)
        monotone_widths.append(monotone_width)
    
    correlation = pearson_correlation(unit_group_sizes, monotone_widths)
    mean_value = sum(unit_group_sizes) / len(unit_group_sizes)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in unit_group_sizes) / len(unit_group_sizes))
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": len(unit_group_sizes),
        "n_max": max(len(circuit) for _ in range(100)),
        "conjecture_holds": abs(correlation) >= 0.8 and abs(correlation - mean_value) <= 3 * std_value,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")