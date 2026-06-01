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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Inverse doesn't exist")
    else:
        return x % m

def polynomial_value(poly, x):
    result = 0
    for coeff in poly:
        result = (result * x + coeff) % m
    return result

def minimal_local_ring_norm(poly, m):
    min_val = float('inf')
    for i in range(m):
        val = polynomial_value(poly, i)
        if val < min_val:
            min_val = val
    return min_val

def dpll_tree_size(formula):
    def dpll(clauses, assignment):
        if not clauses:
            return 1
        if any(all(lit in assignment and assignment[lit] for lit in clause) or all(-lit in assignment and not assignment[-lit] for lit in clause) for clause in clauses):
            return 0
        literal = next(lit for lit in range(1, len(clauses) + 1) if lit not in assignment and -lit not in assignment)
        true_clauses = [c for c in clauses if literal in c]
        false_clauses = [c for c in clauses if -literal in c]
        return dpll(true_clauses, {**assignment, literal: True}) + dpll(false_clauses, {**assignment, literal: False})
    return dpll(formula, {})

def generate_cnf(n):
    num_clauses = random.randint(10, 20)
    clauses = []
    for _ in range(num_clauses):
        clause = [random.choice([-i, i]) for i in range(1, n + 1)]
        if len(set(clause)) == 1:
            continue
        clauses.append(clause)
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    m = 2**random.randint(3, 5)
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        formula = generate_cnf(n)
        min_norm = minimal_local_ring_norm(formula, m)
        tree_size = dpll_tree_size(formula)
        results.append((min_norm, tree_size))
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    min_norms, tree_sizes = zip(*results)
    mean_min_norm = sum(min_norms) / len(min_norms)
    mean_tree_size = sum(tree_sizes) / len(tree_sizes)
    correlation = (sum((min_norm - mean_min_norm) * (tree_size - mean_tree_size) for min_norm, tree_size in results) /
                   math.sqrt(sum((min_norm - mean_min_norm)**2 for min_norm in min_norms) *
                             sum((tree_size - mean_tree_size)**2 for tree_size in tree_sizes)))
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for _, n in results),
        "conjecture_holds": abs(correlation) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(3, 6)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(result["instances_tested"] > 0 for result in results):
        print("RESULT: INCONCLUSIVE reason=not_enough_data n_tested=0")
    else:
        mean_corr = sum(result["metric_value"] for result in results) / len(results)
        std_corr = math.sqrt(sum((result["metric_value"] - mean_corr)**2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if abs(result["metric_value"]) >= 0.7) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not abs(result["metric_value"]) >= 0.7)
            print(f"RESULT: FALSIFIED counterexample='correlation_threshold_not_met' first_failing_seed={first_failing_seed}")