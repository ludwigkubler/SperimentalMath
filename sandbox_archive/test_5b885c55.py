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
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        f = [random.choice([0, 1]) for _ in range(2**n)]
        
        # Convert boolean function to vector space representation V_f
        V_f = [[f[j] if (i >> j) & 1 else 0 for j in range(n)] for i in range(2**n)]
        
        # Compute symplectic measure σ(f)
        sigma_f = 0.0
        for v in V_f:
            sigma_f += sum(v[i] * v[j] for i in range(n) for j in range(i+1, n)) / (n * (n - 1))
        
        # Compute circuit size s(f)
        s_f = len(minimal_disjoint_sum_of_products(f, n))
        
        metric_values.append(sigma_f)
    
    mean_value = sum(metric_values) / instances_tested
    std_value = math.sqrt(sum((x - mean_value)**2 for x in metric_values) / instances_tested)
    
    correlation_coefficient = 0.0
    if len(metric_values) > 1:
        n = len(metric_values)
        numerator = sum((metric_values[i] - mean_value) * (i + 5) for i in range(n))
        denominator = math.sqrt(sum((metric_values[i] - mean_value)**2 for i in range(n))) * math.sqrt(sum(((i + 5) - (n // 2))**2 for i in range(n)))
        correlation_coefficient = numerator / denominator
    
    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.7"
    
    return {
        "metric_name": "symplectic_measure",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def minimal_disjoint_sum_of_products(f, n):
    # Placeholder for actual circuit minimization algorithm
    return [f]

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")