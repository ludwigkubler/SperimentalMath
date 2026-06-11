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
    
    def calculate_lid(f):
        n = int(math.log2(len(f)))
        if n <= 1:
            return 0
        lid = 0
        for i in range(1, n):
            for j in range(i+1, n+1):
                if f[2**i] != f[2**j]:
                    lid += 1
        return lid / (n * (n - 1) // 2)
    
    def calculate_entanglement_complexity(f):
        n = int(math.log2(len(f)))
        complexity = 0
        for i in range(n):
            if f[2**i] != f[2**(i+1)]:
                complexity += 1
        return complexity
    
    lid_values = []
    entanglement_complexity_values = []
    instances_tested = 0
    n_max = 0
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        lid = calculate_lid(f)
        entanglement_complexity = calculate_entanglement_complexity(f)
        
        if lid is not None and entanglement_complexity is not None:
            lid_values.append(lid)
            entanglement_complexity_values.append(entanglement_complexity)
            instances_tested += 1
            n_max = max(n_max, n)
    
    if len(lid_values) == 0 or len(entanglement_complexity_values) == 0:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No valid data points"
        }
    
    correlation_coefficient = sum((x - sum(lid_values) / len(lid_values)) * (y - sum(entanglement_complexity_values) / len(entanglement_complexity_values)) for x, y in zip(lid_values, entanglement_complexity_values)) / (len(lid_values) * math.sqrt(sum((x - sum(lid_values) / len(lid_values))**2 for x in lid_values)) * math.sqrt(sum((y - sum(entanglement_complexity_values) / len(entanglement_complexity_values))**2 for y in entanglement_complexity_values)))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")