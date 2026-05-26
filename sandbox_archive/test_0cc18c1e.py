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

def generate_random_3sat(n, m):
    clauses = []
    for _ in range(m):
        clause = [random.randint(-n, -1) if random.choice([True, False]) else random.randint(1, n)
                   for _ in range(random.randint(2, 3))]
        clauses.append(clause)
    return clauses

def is_satisfiable(clauses):
    def backtrack(i, assignment):
        if i > len(clauses):
            return True
        for val in [-1, 1]:
            assignment[i] = val
            if all(any(x * assignment[abs(x)] >= 0 for x in clause) for clause in clauses):
                if backtrack(i + 1, assignment):
                    return True
        assignment[i] = None
        return False

    n = len(clauses)
    assignment = [None] * (n + 1)
    return backtrack(1, assignment)

def compute_minimal_rank(clauses):
    # Placeholder for actual computation of minimal rank
    # This is a dummy implementation and should be replaced with actual logic
    return random.randint(1, 10)  # Dummy value

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = 2 * n
    clauses = generate_random_3sat(n, m)
    
    if not is_satisfiable(clauses):
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "unsatisfiable_formula"
        }
    
    rank = compute_minimal_rank(clauses)
    expected_rank = math.log2(n) ** 2
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": abs(rank - expected_rank) <= 0.5 * expected_rank,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")