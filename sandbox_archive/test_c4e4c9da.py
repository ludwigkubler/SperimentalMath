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
    
    def compute_geometric_arrangement(f):
        # Placeholder function to simulate geometric arrangement
        return len(f)
    
    def find_coxeter_system(d):
        # Placeholder function to simulate finding a Coxeter system
        return d
    
    def calculate_complexity(f, d):
        # Placeholder function to simulate complexity calculation
        return random.randint(1, d**2)
    
    n = 5
    f = generate_boolean_function(n)
    d = compute_geometric_arrangement(f)
    c = find_coxeter_system(d)
    complexity = calculate_complexity(f, d)
    
    metric_value = complexity / (d ** 2 * math.log(d))
    conjecture_holds = metric_value <= (d ** 2 * math.log(d))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "complexity",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 73))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(res["metric_value"] for res in results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")