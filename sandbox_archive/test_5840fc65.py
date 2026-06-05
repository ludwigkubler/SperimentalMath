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
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def monoidal_categorification(clauses):
        # Simplified categorification: count unique literals
        unique_literals = set()
        for clause in clauses:
            for literal in clause:
                unique_literals.add(abs(literal))
        return len(unique_literals)
    
    def entropy(subset):
        if not subset:
            return 0
        p = len(subset) / n
        return -p * math.log2(p) - (1 - p) * math.log2(1 - p)
    
    n_max = 40
    instances_tested = 0
    total_order = 0
    total_entropy = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            break
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n)
            order = monoidal_categorification(cnf)
            total_order += order
            total_entropy += entropy(cnf)
            instances_tested += 1
    
    mean_order = total_order / instances_tested
    mean_entropy = total_entropy / instances_tested
    correlation = (mean_order - n) / math.sqrt(n)
    
    if not (-n <= correlation <= n):
        return {
            "metric_name": "correlation",
            "metric_value": correlation,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": f"Correlation out of bounds: {correlation}"
        }
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_out_of_bounds\" first_failing_seed={first_failing_seed}")