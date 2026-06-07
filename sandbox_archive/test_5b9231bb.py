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
    
    def dpll(instance, assignment):
        if not instance:
            return True
        var = next(iter(instance))
        for val in [True, False]:
            new_assignment = assignment.copy()
            new_assignment[var] = val
            if dpll(instance - {var}, new_assignment):
                return True
        return False
    
    def generate_instance(n: int) -> dict:
        instance = {}
        for _ in range(n):
            var = random.choice(list(assignment.keys()))
            val = random.choice([True, False])
            instance[var] = val
        return instance
    
    assignment = {f'x{i}': None for i in range(10)}
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    
    for n in n_values:
        instances_tested = 0
        path_lengths = []
        
        while len(path_lengths) < 30:
            instance = generate_instance(n)
            if dpll(instance, assignment):
                path_length = sum(1 for _ in instance.keys())
                path_lengths.append(path_length)
                instances_tested += 1
        
        metric_values.extend(path_lengths)
    
    n_max = max(n_values)
    conjecture_holds = False
    counterexample = ""
    
    if len(metric_values) >= 30:
        # Calculate Pearson correlation coefficient
        mean_x = sum(metric_values) / len(metric_values)
        mean_y = mean_x  # Assuming linear relationship for simplicity
        numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(range(len(metric_values)), metric_values))
        denominator = math.sqrt(sum((x - mean_x) ** 2 for x in range(len(metric_values)))) * math.sqrt(sum((y - mean_y) ** 2 for y in metric_values))
        correlation_coefficient = numerator / denominator if denominator != 0 else 0
        
        # Check if the correlation coefficient is significant
        t_statistic = correlation_coefficient * math.sqrt((len(metric_values) - 2) / (1 - correlation_coefficient ** 2))
        p_value = 2 * (1 - 0.5 * (1 + math.erf(t_statistic / math.sqrt(2))))
        
        if correlation_coefficient >= 0.7 and p_value <= 0.05:
            conjecture_holds = True
        else:
            counterexample = f"Correlation coefficient: {correlation_coefficient}, p-value: {p_value}"
    
    return {
        "metric_name": "DPLL Proof Tree Path Length",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": len(metric_values),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    # Compute mean/std of metric_value and fraction of seeds where conjecture_holds
    all_results = [run_trial(seed) for seed in seeds]
    mean_metric_value = sum(result["metric_value"] for result in all_results) / len(all_results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in all_results) / len(all_results))
    support_fraction = sum(1 for result in all_results if result["conjecture_holds"]) / len(all_results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in all_results):
        first_failing_seed = next(seed for seed, result in zip(seeds, all_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")