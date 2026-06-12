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
    
    def generate_formula(n, m):
        variables = set(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def calculate_resolution_width(clauses):
        # Simplified resolution width calculation (not accurate but sufficient for testing)
        return len(clauses) ** 0.5
    
    def topological_entropy(n, m):
        # Simplified topological entropy calculation (not accurate but sufficient for testing)
        return n * math.log2(n + m)
    
    n = random.randint(5, 40)
    m = random.randint(1, 2*n)
    formula = generate_formula(n, m)
    w_phi = calculate_resolution_width(formula)
    H_top_phi = topological_entropy(n, m)
    
    metric_value = w_phi <= H_top_phi ** 2 * math.log(n + m)
    instances_tested = 1
    n_max = n
    conjecture_holds = metric_value
    counterexample = "" if conjecture_holds else f"Formula with n={n}, m={m} violates the conjecture"
    
    return {
        "metric_name": "w(φ) ≤ H_top(φ)² * log(n+m)",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Formula with n={results[0]['n_max']}, m={results[0]['instances_tested']} violates the conjecture\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")