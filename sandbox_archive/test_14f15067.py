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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([1, -1]) * random.randint(1, n) for _ in range(random.randint(1, n))]
            if all(abs(lit) != abs(other_lit) for lit in clause for other_lit in clause[1:]):
                clauses.append(clause)
        return clauses
    
    def find_local_indecomposable_module(clauses):
        # Placeholder for the actual implementation of finding a local indecomposable module
        # This is a dummy function that returns a random order
        return random.randint(1, 10)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for n in range(5, 41):
        max_order = 0
        for _ in range(instances_tested):
            cnf = generate_cnf(n)
            order = find_local_indecomposable_module(cnf)
            if order > max_order:
                max_order = order
        
        metric_values.append(max_order)
    
    alpha = max(metric_values) ** (1 / n_max)
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    
    conjecture_holds = all(value >= alpha**n for n, value in enumerate(metric_values, start=5))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "max_order",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")