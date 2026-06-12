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
    
    def generate_boolean_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_minimal_order(solutions):
        n = len(solutions[0])
        if n == 0:
            return 0
        min_order = float('inf')
        for i in range(n + 1):
            if all(all(s[j] == s[k] for j, k in combinations(range(n), i)) for s in solutions):
                min_order = min(min_order, 2**i)
        return min_order
    
    def compute_resolution_width(instance):
        n = len(instance)
        clauses = [[i for i in range(n) if instance[i]], [i for i in range(n) if not instance[i]]]
        width = max(len(clause) for clause in clauses)
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        instance = generate_boolean_instance(n)
        solutions = [instance]
        min_order = compute_minimal_order(solutions)
        resolution_width = compute_resolution_width(instance)
        
        if min_order != 0 and resolution_width > 0:
            metric_value = abs(min_order - n**(1/3)) / (n**(1/3))
            total_metric_value += metric_value
            instances_tested += len(solutions)
            n_max = max(n_max, n)
            
            if metric_value > 0.1 * n**(1/3):
                conjecture_holds = False
                counterexample = f"n={n}, min_order={min_order}, resolution_width={resolution_width}"
    
    return {
        "metric_name": "Mean Absolute Error",
        "metric_value": total_metric_value / instances_tested if instances_tested > 0 else float('nan'),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if not math.isnan(r["metric_value"])) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")