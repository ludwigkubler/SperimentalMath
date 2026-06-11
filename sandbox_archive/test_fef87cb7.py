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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(k):
    primes = []
    num = 2
    while len(primes) < k:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def random_cnf(n, m):
    cnf = set()
    for _ in range(m):
        literals = [random.choice([1, -1]) * (i + 1) for i in range(n)]
        clause = tuple(sorted(literals))
        if clause not in cnf:
            cnf.add(clause)
    return cnf

def generate_satisfying_assignments(cnf, n):
    satisfying_assignments = set()
    while len(satisfying_assignments) < 30:
        assignment = [random.choice([0, 1]) for _ in range(n)]
        if all(any(lit == assignment[abs(lit) - 1] * sign for lit, sign in clause) for clause in cnf):
            satisfying_assignments.add(tuple(assignment))
    return satisfying_assignments

def compute_quotient_group_order(satisfying_assignments):
    n = len(satisfying_assignments)
    if n < 2:
        return None
    kernel = set()
    for i in range(n):
        for j in range(i + 1, n):
            if all(assignment[i] == assignment[j] for assignment in satisfying_assignments):
                kernel.add((i, j))
    quotient_group_order = len(kernel) + 1
    return quotient_group_order

def run_trial(seed: int) -> dict:
    random.seed(seed)
    cnf = random_cnf(5, 10)  # Generate a random CNF with 5 variables and 10 clauses
    satisfying_assignments = generate_satisfying_assignments(cnf, 5)
    quotient_group_order = compute_quotient_group_order(satisfying_assignments)
    
    if quotient_group_order is None:
        return {
            "metric_name": "quotient_group_order",
            "metric_value": None,
            "instances_tested": len(satisfying_assignments),
            "n_max": 5,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    # Placeholder for Frege proof depth calculation
    frege_proof_depth = random.randint(10, 20)  # Simplified placeholder
    
    return {
        "metric_name": "quotient_group_order",
        "metric_value": quotient_group_order,
        "instances_tested": len(satisfying_assignments),
        "n_max": 5,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(isinstance(r["metric_value"], (int, float)) and r["conjecture_holds"] is False for r in results):
        RESULT = "INCONCLUSIVE mapping_undefined"
    else:
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        RESULT = f"SUPPORTED mean={mean_metric_value:.4f} std={std_metric_value:.4f} support_fraction={support_fraction:.2f}"
    
    print(RESULT)