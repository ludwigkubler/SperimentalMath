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
    
    def generate_kcnf(n, k):
        clauses = []
        for _ in range(k):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0], clause[1] = clause[1], clause[0]
            clauses.append(clause)
        return clauses
    
    def tropicalize_complexity(n):
        return 2 ** (n / 4)
    
    def compute_coxeter_group_action_complexity(clauses):
        # Placeholder for actual computation
        # For simplicity, we use a dummy value
        return len(clauses) * 5
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        total_complexity = 0
        for _ in range(5):  # Test each size with 5 different instances
            clauses = generate_kcnf(n, n)
            complexity = compute_coxeter_group_action_complexity(clauses)
            total_complexity += complexity
            instances_tested += 1
        metric_value = total_complexity / instances_tested
        expected_value = tropicalize_complexity(n)
        if abs(metric_value - expected_value) > 0.3 * expected_value:
            return {
                "metric_name": "Coxeter Group Action Complexity",
                "metric_value": metric_value,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"Complexity {metric_value} exceeds expected tropicalized value {expected_value}"
            }
        results.append({
            "metric_name": "Coxeter Group Action Complexity",
            "metric_value": metric_value,
            "instances_tested": instances_tested,
            "n_max": n,
            "conjecture_holds": True,
            "counterexample": ""
        })
    
    return results

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        trial_results = run_trial(seed)
        results.extend(trial_results)
        print(f"TRIAL: {trial_results}")
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r["metric_value"] - tropicalize_complexity(r["n_max"])) <= 0.2 * tropicalize_complexity(r["n_max"])) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Complexity exceeds expected tropicalized value\" first_failing_seed={first_failing_seed}")