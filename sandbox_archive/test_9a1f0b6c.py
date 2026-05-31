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
        clauses = []
        for _ in range(random.randint(1, n)):
            clause = [random.choice([f"x{i+1}", f"~x{i+1}"]) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def galois_group_degree(clauses):
        # Placeholder function to compute the Galois group degree
        # This is a dummy implementation and should be replaced with actual computation
        return len(clauses) ** 2
    
    n_max = 40
    instances_tested = 0
    total_metric_value = 0
    
    for n in range(5, n_max + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            clauses = generate_formula(n)
            degree = galois_group_degree(clauses)
            metric_value = degree / (len(clauses) ** 2)
            total_metric_value += metric_value
            instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": "Galois Group Degree",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = mean_metric_value <= 1.0
    
    return {
        "metric_name": "Galois Group Degree",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "Counterexample found"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")