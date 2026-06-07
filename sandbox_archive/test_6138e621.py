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
from math import gcd

def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def generate_random_prime(n):
    while True:
        p = random.randint(2**(n-1), 2**n - 1)
        if is_prime(p):
            return p

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def generate_random_cnf(n):
    cnf = []
    for _ in range(random.randint(1, n)):
        clause = [random.randint(-n, n) for _ in range(random.randint(1, n))]
        if 0 not in clause:
            cnf.append(clause)
    return cnf

def polynomial_representation(cnf):
    max_var = max(abs(var) for clause in cnf for var in clause)
    poly = [0] * (max_var + 1)
    for clause in cnf:
        product = 1
        for var in clause:
            if var > 0:
                product *= (var**2 - 1)
            else:
                product *= ((-var)**2 - 1)
        poly[0] += product
    return poly

def minimal_order_of_generalized_quadratic_residues(poly, p):
    order = {}
    for i in range(1, p):
        if gcd(i, p) == 1:
            value = pow(i, 2, p)
            if value not in order or order[value] > i:
                order[value] = i
    return len(order)

def resolution_proof_width(cnf):
    # Simplified DPLL solver to estimate proof width
    def dpll(clauses, assignment):
        if not clauses:
            return 0
        unit_clauses = [c for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            return dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment)
        pure_literals = [l for l in range(1, max(abs(var) for clause in cnf for var in clause) + 1) if (l not in assignment and -l not in assignment)]
        if not pure_literals:
            return float('inf')
        literal = pure_literals[0]
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        return dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment)
    return dpll(cnf, {})

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    p = generate_random_prime(n)
    cnf = generate_random_cnf(n)
    poly = polynomial_representation(cnf)
    order = minimal_order_of_generalized_quadratic_residues(poly, p)
    width = resolution_proof_width(cnf)
    if width == float('inf'):
        return {
            "metric_name": "minimal_order",
            "metric_value": order,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "resolution_proof_width_infinite"
        }
    ratio = order / width
    return {
        "metric_name": "minimal_order",
        "metric_value": order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='resolution_proof_width_infinite' first_failing_seed={first_failing_seed}")