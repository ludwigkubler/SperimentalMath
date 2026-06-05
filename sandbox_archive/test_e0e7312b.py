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
    
    def generate_quasi_random_sequence(n):
        return [random.randint(0, 1) for _ in range(n)]
    
    def binary_string_to_boolean_function(binary_string):
        n = len(binary_string)
        return lambda x: 1 if x == int(''.join(str(bit) for bit in binary_string), 2) else 0
    
    def circuit_monotone_width(f, n):
        max_depth = 0
        visited = [False] * (2 ** n)
        
        def dfs(x, depth):
            nonlocal max_depth
            if x >= 2 ** n:
                return
            if not visited[x]:
                visited[x] = True
                max_depth = max(max_depth, depth)
                for i in range(n):
                    dfs(2 * x + binary_string[i], depth + 1)
        
        dfs(0, 0)
        return max_depth
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        sequence = generate_quasi_random_sequence(n)
        binary_string = ''.join(str(bit) for bit in sequence)
        f = binary_string_to_boolean_function(binary_string)
        width = circuit_monotone_width(f, n)
        results.append((n, width))
    
    if len(results) < 30:
        return {
            "metric_name": "circuit_monotone_width",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _ in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    total_width = sum(width for _, width in results)
    mean_width = Fraction(total_width, len(results))
    std_deviation = math.sqrt(sum((width - mean_width) ** 2 for _, width in results) / len(results))
    
    return {
        "metric_name": "circuit_monotone_width",
        "metric_value": float(mean_width),
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": mean_width > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2**i - 1 for i in range(1, 31)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_deviation = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_deviation} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_conjecture_holds")