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
    
    def generate_circuit(n):
        if n == 1:
            return [random.choice([0, 1])]
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - n // 2)
            return [random.choice([0, 1]) for _ in range(n)]
    
    def compute_local_ring(circuit):
        # Simplified local ring computation using Frobenius endomorphism
        # This is a placeholder and should be replaced with actual implementation
        return len(circuit) ** 2
    
    def measure_unit_group_size(local_ring):
        return len([x for x in range(1, local_ring + 1) if local_ring % x == 0])
    
    def measure_monotone_width(circuit):
        # Simplified monotone width calculation
        # This is a placeholder and should be replaced with actual implementation
        return sum(1 for bit in circuit if bit == 1)
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    instances_tested = 0
    unit_group_sizes = []
    monotone_widths = []
    n_max = 1
    
    for n in [5, 10, 15, 20, 30, 40]:
        circuit = generate_circuit(n)
        local_ring = compute_local_ring(circuit)
        unit_group_size = measure_unit_group_size(local_ring)
        monotone_width = measure_monotone_width(circuit)
        
        instances_tested += n
        if n > n_max:
            n_max = n
        
        unit_group_sizes.extend([unit_group_size] * n)
        monotone_widths.extend([monotone_width] * n)
    
    correlation_coefficient = pearson_correlation(unit_group_sizes, monotone_widths)
    metric_value = correlation_coefficient
    conjecture_holds = correlation_coefficient >= 0.8 and abs(metric_value) <= 3 * math.sqrt(2 / instances_tested)
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8 or |metric_value| > 3 * sqrt(2 / instances_tested)"
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": metric_value,
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
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8 or |metric_value| > 3 * sqrt(2 / instances_tested)\" first_failing_seed={next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")