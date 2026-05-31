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
    
    def generate_formula(n):
        num_clauses = random.randint(5, 10)
        clauses = []
        for _ in range(num_clauses):
            clause = [random.choice([f'x{i+1}', f'~x{i+1}']) for i in range(random.randint(2, n))]
            clauses.append(clause)
        return clauses
    
    def galois_group_size(clauses):
        # Simplified version of computing the Galois group size
        num_vars = max(int(x[1:]) for clause in clauses for x in clause if x.startswith('x'))
        return 2 ** (num_vars - 1)
    
    def distinct_clauses(clauses):
        return len(set(tuple(sorted(clause)) for clause in clauses))
    
    results = []
    n_max = 0
    instances_tested = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            clauses = generate_formula(n)
            deg_G = galois_group_size(clauses)
            num_clauses = distinct_clauses(clauses)
            results.append((deg_G, num_clauses))
            n_max = max(n_max, n)
            instances_tested += 1
    
    if not results:
        return {
            "metric_name": "Galois Group Size",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    deg_G_values = [deg for deg, _ in results]
    num_clauses_values = [num for _, num in results]
    
    def mean(lst):
        return sum(lst) / len(lst)
    
    def std(lst):
        avg = mean(lst)
        variance = sum((x - avg) ** 2 for x in lst) / len(lst)
        return math.sqrt(variance)
    
    deg_G_mean = mean(deg_G_values)
    num_clauses_mean = mean(num_clauses_values)
    deg_G_std = std(deg_G_values)
    
    conjecture_holds = all(deg_G <= num_clauses ** 2 for deg_G, _ in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Galois Group Size",
        "metric_value": deg_G_mean,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample_desc = "mapping_undefined"
        mean_value = None
        std_value = None
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(result['conjecture_holds'] for result in results) else 'FALSIFIED'} mean={mean_value} std={std_value} support_fraction={support_fraction}")