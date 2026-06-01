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
    
    def generate_circuits(n):
        circuits = []
        for _ in range(100):  # Generate 100 circuits per n
            depth = random.randint(2, n // 2)
            circuit = [random.choice([0, 1]) for _ in range(depth)]
            circuits.append(circuit)
        return circuits
    
    def compute_local_ring(circuit):
        # Simplified negacyclic representation using XOR
        local_ring = set()
        for x in range(2 ** len(circuit)):
            if all((x >> i) & 1 == circuit[i] for i in range(len(circuit))):
                local_ring.add(x)
        return local_ring
    
    def measure_unit_group_size(local_ring):
        # Minimal size of the unit group
        return len(local_ring)
    
    def measure_monotone_width(circuit):
        # Monotone width is the maximum number of gates on any path from input to output
        max_width = 0
        for i in range(len(circuit)):
            width = sum(1 for j in range(i) if circuit[j] == circuit[i])
            max_width = max(max_width, width)
        return max_width
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        circuits = generate_circuits(n)
        unit_group_sizes = []
        monotone_widths = []
        
        for circuit in circuits:
            local_ring = compute_local_ring(circuit)
            unit_group_size = measure_unit_group_size(local_ring)
            monotone_width = measure_monotone_width(circuit)
            
            unit_group_sizes.append(unit_group_size)
            monotone_widths.append(monotone_width)
        
        correlation = pearson_correlation(unit_group_sizes, monotone_widths)
        results.append({
            "n": n,
            "correlation": correlation
        })
    
    mean_corr = sum(result["correlation"] for result in results) / len(results)
    std_corr = math.sqrt(sum((result["correlation"] - mean_corr) ** 2 for result in results) / len(results))
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": mean_corr,
        "instances_tested": sum(len(result["unit_group_sizes"]) for result in results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": mean_corr >= 0.8 and abs(mean_corr) <= 3 * std_corr,
        "counterexample": "" if mean_corr >= 0.8 else "Pearson correlation < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_corr = sum(result["metric_value"] for result in results) / len(results)
    std_corr = math.sqrt(sum((result["metric_value"] - mean_corr) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation < 0.8\" first_failing_seed={first_failing_seed}")