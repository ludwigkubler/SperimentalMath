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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def ehrhart_cohomology_rank(f):
        n = int(math.log2(len(f)))
        # Simplified Ehrhart cohomology rank calculation
        return n
    
    def randomized_or_complexity(f):
        n = int(math.log2(len(f)))
        max_bits = 0
        for _ in range(100):  # Sample 100 random inputs
            input_bits = ''.join(str(bit) for bit in random.choice(f))
            bits_needed = len(input_bits)
            if bits_needed > max_bits:
                max_bits = bits_needed
        return max_bits
    
    n_values = [5, 10, 15, 20, 30, 40]
    data_points = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        rank = ehrhart_cohomology_rank(f)
        complexity = randomized_or_complexity(f)
        data_points.append((rank**2, complexity))
    
    if not data_points:
        return {
            "metric_name": "ROR_f vs Ehrhart Rank^2",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    x = [dp[0] for dp in data_points]
    y = [dp[1] for dp in data_points]
    n = len(x)
    
    if n < 30:
        return {
            "metric_name": "ROR_f vs Ehrhart Rank^2",
            "metric_value": None,
            "instances_tested": n,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))
    sum_xx = sum(xi**2 for xi in x)
    
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x**2)
    
    return {
        "metric_name": "ROR_f vs Ehrhart Rank^2",
        "metric_value": slope,
        "instances_tested": n,
        "conjecture_holds": slope <= 1,  # Assuming c = 1 for simplicity
        "counterexample": "" if slope <= 1 else f"Counterexample found with slope {slope}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        mean = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / sum(1 for r in results if r["conjecture_holds"])
        std = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results if r["conjecture_holds"]) / sum(1 for r in results if r["conjecture_holds"]))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(r['conjecture_holds'] for r in results) else 'FALSIFIED'} mean={mean} std={std} support_fraction={support_fraction}")