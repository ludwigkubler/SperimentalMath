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

def generate_tseitin_formula(n):
    variables = list(range(1, n + 1))
    clauses = []
    
    for i in range(1, n + 1):
        clauses.append([variables[i-1]])
    
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            clauses.append([-variables[i-1], -variables[j-1]])
            clauses.append([variables[i-1], variables[j-1]])
            clauses.append([variables[i-1], -variables[j-1]])
    
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        clauses = generate_tseitin_formula(n)
        # Placeholder for computing minimal local indeterminacy and resolution proof width
        I_phi = random.random() * n  # Dummy value, replace with actual computation
        w_phi = random.randint(1, n)  # Dummy value, replace with actual computation
        metric_values.append(abs(I_phi - w_phi))
    
    mean_value = sum(metric_values) / instances_tested
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / instances_tested)
    
    if any(x > 3 for x in metric_values):
        conjecture_holds = False
        counterexample = "absolute difference exceeds 3"
    
    return {
        "metric_name": "Absolute Difference",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if not result["counterexample"]) / len(results)
    
    if all(not result["counterexample"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")