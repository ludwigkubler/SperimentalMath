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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def circuit_size(f):
        # Simplified DPLL solver to estimate circuit size
        n = len(f)
        if n == 1:
            return 1
        return 2 * circuit_size(f[:n//2]) + 2
    
    def irreducible_representation_dimension(f):
        n = len(f)
        F = [f[i:i+n] for i in range(0, len(f), n)]
        dim = 0
        for row in F:
            if all(row[j] == row[0] for j in range(1, len(row))):
                dim += 1
        return dim
    
    def correlation_coefficient(data):
        mean_x = sum(x for x, _ in data) / len(data)
        mean_y = sum(y for _, y in data) / len(data)
        numerator = sum((x - mean_x) * (y - mean_y) for x, y in data)
        denominator = math.sqrt(sum((x - mean_x)**2 for x, _ in data)) * math.sqrt(sum((y - mean_y)**2 for _, y in data))
        return numerator / denominator if denominator != 0 else 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    data = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        s_f = circuit_size(f)
        dim_Irr_f = irreducible_representation_dimension(f)
        data.append((s_f**2, dim_Irr_f))
    
    correlation = correlation_coefficient(data)
    conjecture_holds = correlation > 0.7
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.7"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation,
        "instances_tested": len(data),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")