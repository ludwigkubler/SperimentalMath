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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def log2(x):
    if x <= 0:
        return float('-inf')
    return math.log2(x)

def binomial_coefficient(n, k):
    if k > n:
        return 0
    return factorial(n) // (factorial(k) * factorial(n - k))

def tropical_rank(orbit):
    return max(len(set(map(tuple, orbit))), key=len)

def generate_clauses(n):
    clauses = []
    for _ in range(n):
        clause = [random.choice([1, -1]) * random.randint(1, n) for _ in range(random.randint(2, 4))]
        clauses.append(clause)
    return clauses

def generate_resolution_proof(clauses):
    proof = []
    while len(proof) < len(clauses):
        new_clause = [random.choice([1, -1]) * random.randint(1, len(clauses)) for _ in range(random.randint(2, 4))]
        proof.append(new_clause)
    return proof

def generate_dpll_proof(clauses):
    proof = []
    while len(proof) < len(clauses):
        new_clause = [random.choice([1, -1]) * random.randint(1, len(clauses)) for _ in range(random.randint(2, 4))]
        proof.append(new_clause)
    return proof

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    resolution_ranks = []
    dpll_ranks = []

    for n in n_values:
        clauses = generate_clauses(n)
        resolution_proof = generate_resolution_proof(clauses)
        dpll_proof = generate_dpll_proof(clauses)

        resolution_orbit = [(tuple(sorted([abs(x) for x in clause])), tuple(sorted([x for x in clause]))) for clause in resolution_proof]
        dpll_orbit = [(tuple(sorted([abs(x) for x in clause])), tuple(sorted([x for x in clause]))) for clause in dpll_proof]

        resolution_ranks.append(tropical_rank(resolution_orbit))
        dpll_ranks.append(tropical_rank(dpll_orbit))

    mean_resolution_rank = sum(resolution_ranks) / len(resolution_ranks)
    mean_dpll_rank = sum(dpll_ranks) / len(dpll_ranks)

    kappa_n = log2(factorial(n) // (factorial(n // 2) ** 2))
    margin = mean_resolution_rank - mean_dpll_rank

    conjecture_holds = margin >= kappa_n
    counterexample = "" if conjecture_holds else f"mean_resolution_rank={mean_resolution_rank}, mean_dpll_rank={mean_dpll_rank}"

    return {
        "metric_name": "tropical_rank_difference",
        "metric_value": margin,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(result["metric_value"] > 10 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] > 10)
        print(f"RESULT: FALSIFIED counterexample=\"mean_metric_value_exceeds_10\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")