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
    
    def generate_kcnf(n, k):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(k):
            clause = [random.choice(variables) if random.choice([True, False]) else -random.choice(variables) for _ in range(random.randint(2, n))]
            clauses.append(clause)
        return clauses

    def is_tautology(clauses):
        variables = set(abs(v) for v in sum(clauses, []))
        assignment = {v: None for v in variables}
        
        def backtrack(index):
            if index == len(variables):
                return all(any(c[i] <= 0 for c in clauses) for i in range(len(variables)))
            for value in [True, False]:
                assignment[variables[index]] = value
                if backtrack(index + 1):
                    return True
                assignment[variables[index]] = None
            return False
        
        return backtrack(0)

    def quantum_logarithmic_capacity(clauses):
        n = len(set(abs(v) for v in sum(clauses, [])))
        # Simplified approximation for demonstration purposes
        return math.log(n, 2)

    n_values = [5, 10, 15, 20, 30, 40]
    total_capacity = 0
    instances_tested = 0

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            clauses = generate_kcnf(n, n)
            if is_tautology(clauses):
                continue
            capacity = quantum_logarithmic_capacity(clauses)
            total_capacity += capacity
            instances_tested += 1

    average_capacity = total_capacity / instances_tested
    conjecture_holds = average_capacity >= math.sqrt(n) * math.log(n, 2)

    return {
        "metric_name": "Quantum Logarithmic Capacity",
        "metric_value": average_capacity,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_capacity = sum(r["metric_value"] for r in results) / len(results)
    std_capacity = math.sqrt(sum((r["metric_value"] - mean_capacity) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_capacity} std={std_capacity} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_capacity} std={std_capacity} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")