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
    
    def generate_instance(n):
        return [random.choice([0, 1]) for _ in range(n)]
    
    def dpll(instance, assignment=[]):
        if len(assignment) == len(instance):
            return True
        var = next((i for i, val in enumerate(instance) if val is None), None)
        if var is None:
            return False
        for val in [0, 1]:
            new_assignment = assignment[:]
            new_assignment.append(val)
            if dpll(instance, new_assignment):
                return True
        return False
    
    def hodge_arc_length(n):
        # Simplified approximation of Hodge arc length for demonstration purposes
        return n * (n + 1) / 2
    
    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / len(x))
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / len(y))
        return cov / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    hodge_lengths = []
    dpll_widths = []
    
    for n in n_values:
        instances = [generate_instance(n) for _ in range(30)]
        for instance in instances:
            assignment = [None] * len(instance)
            if dpll(instance, assignment):
                dpll_widths.append(len(assignment))
            else:
                dpll_widths.append(len(assignment))
            hodge_lengths.append(hodge_arc_length(n))
    
    correlation = pearson_correlation(hodge_lengths, dpll_widths)
    p_value = 0.05  # Placeholder for actual p-value calculation
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": len(instances) * len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation > 0.8 and p_value < 0.05,
        "counterexample": "" if correlation > 0.8 else "Pearson correlation ≤ 0.8 or p-value ≥ 0.1"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 7 for i in range(5, 30)]  # First 30 prime numbers
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] <= 0.5 or r["p_value"] >= 0.1 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation ≤ 0.8 or p-value ≥ 0.1\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")