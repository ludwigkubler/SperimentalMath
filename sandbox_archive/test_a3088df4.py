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
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def next_prime(n):
    if n <= 1:
        return 2
    candidate = n
    found = False
    while not found:
        candidate += 1
        if is_prime(candidate):
            found = True
    return candidate

def minimal_quadratic_residue_symbol(p):
    if p % 4 != 1:
        return None
    for zeta in range(2, p):
        if (zeta * zeta) % (p * p) == 1:
            return zeta
    return None

def generate_k_cnf(n, k):
    clauses = []
    variables = list(range(1, n + 1))
    for _ in range(k):
        clause = random.sample(variables, random.randint(1, n))
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)
    return clauses

def dpll_search_tree_height(clauses):
    def dpll(clauses, assignment):
        if not clauses:
            return 0
        unit_clauses = [c[0] for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if literal < 0:
                new_assignment[-literal] = False
            return 1 + dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment)
        pure_literals = [l for l, count in Counter(lit for clause in clauses for lit in clause).items() if count == len(clauses)]
        if pure_literals:
            literal = pure_literals[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if literal < 0:
                new_assignment[-literal] = False
            return 1 + dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment)
        literal, _ = min((sum(1 for clause in clauses if lit in clause), lit) for lit in variables + [-v for v in variables])
        new_assignment_true = assignment.copy()
        new_assignment_true[literal] = True
        if literal < 0:
            new_assignment_true[-literal] = False
        true_height = dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment_true)
        new_assignment_false = assignment.copy()
        new_assignment_false[literal] = False
        if literal < 0:
            new_assignment_false[-literal] = True
        false_height = dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment_false)
        return 1 + max(true_height, false_height)
    return dpll(clauses, {})

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        primes = [p for p in range(n, 1000) if is_prime(p)]
        log_zeta_min_sum = 0
        instances_tested = 0
        for _ in range(5):
            k_log_n = random.randint(int(0.2 * n), int(0.8 * n))
            clauses = generate_k_cnf(n, k_log_n)
            height = dpll_search_tree_height(clauses)
            if height is not None:
                instances_tested += 1
                log_zeta_min = math.log2(minimal_quadratic_residue_symbol(next_prime(n)))
                if log_zeta_min is not None:
                    log_zeta_min_sum += log_zeta_min
        if instances_tested > 0:
            mean_log_zeta_min = log_zeta_min_sum / instances_tested
            results.append({"n": n, "instances_tested": instances_tested, "mean_log_zeta_min": mean_log_zeta_min})
    if not results:
        return {
            "metric_name": "DPLL Search Tree Height",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    mean_height = sum(result["instances_tested"] * result["mean_log_zeta_min"] for result in results) / sum(result["instances_tested"] for result in results)
    n_max = max(result["n"] for result in results)
    conjecture_holds = all(result["instances_tested"] > 0 and result["mean_log_zeta_min"] >= mean_height for result in results)
    counterexample = "" if conjecture_holds else "DPLL tree height exceeds log(ζ_min(p)) for some instances"
    return {
        "metric_name": "DPLL Search Tree Height",
        "metric_value": mean_height,
        "instances_tested": sum(result["instances_tested"] for result in results),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        print(f"TRIAL: {run_trial(seed)}")
        results.append(run_trial(seed))
    
    mean_value = sum(result["metric_value"] * result["instances_tested"] for result in results) / sum(result["instances_tested"] for result in results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 * result["instances_tested"] for result in results) / sum(result["instances_tested"] for result in results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and sum(1 for result in results if not result["conjecture_holds"]) / len(results) <= 0.2:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"DPLL tree height exceeds log(ζ_min(p))\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data n_tested={len(results)}")