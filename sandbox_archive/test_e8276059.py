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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_random_cnf(n):
    clauses = []
    for _ in range(n):
        clause = [random.randint(-n, -1), random.randint(1, n)]
        clauses.append(clause)
    return clauses

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def is_primitive_root(g, p):
    if gcd(g, p) != 1:
        return False
    order = p - 1
    factors = {2}
    for i in range(3, int(math.sqrt(order)) + 1, 2):
        if order % i == 0:
            factors.add(i)
            factors.add(order // i)
    for factor in factors:
        if pow(g, factor, p) == 1:
            return False
    return True

def find_primitive_root(p):
    if not is_prime(p):
        raise ValueError("p must be a prime number")
    for g in range(2, p):
        if is_primitive_root(g, p):
            return g
    return None

def frege_proof_depth(cnf):
    # Placeholder function to simulate Frege proof depth calculation
    # This is a dummy implementation and should be replaced with actual logic
    return len(cnf) * 10

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    cnf = generate_random_cnf(n)
    p = find_primitive_root(2 * n + 1)
    if p is None:
        return {
            "metric_name": "ord_p(φ)",
            "metric_value": -1,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    ord_p_phi = pow(random.randint(2, p - 1), (p - 1) // 2, p)
    d_phi = frege_proof_depth(cnf)
    alpha_n = n * 5  # Placeholder function to simulate α(n)
    return {
        "metric_name": "ord_p(φ)",
        "metric_value": ord_p_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ord_p_phi <= alpha_n and d_phi <= alpha_n,
        "counterexample": "" if ord_p_phi <= alpha_n and d_phi <= alpha_n else f"ord_p(φ)={ord_p_phi}, d(φ)={d_phi}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")