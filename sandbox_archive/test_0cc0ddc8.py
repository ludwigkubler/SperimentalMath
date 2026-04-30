# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return (gcd, x, y)

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Inverse doesn't exist")
    else:
        return x % m

def polynomial_to_cnf(poly, n):
    cnf = []
    for term in poly:
        clause = [term[i] * (-1) ** (i % 2) for i in range(n)]
        cnf.append(clause)
    return cnf

def dpll_search_tree_size(cnf):
    def dpll(clauses, assignment):
        if not clauses:
            return 0
        if any(all(lit in assignment and assignment[lit] == val for lit, val in clause) for clause in clauses):
            return 0
        literals = [lit for clause in clauses for lit in clause if lit not in assignment]
        literal = literals[0]
        new_clauses = []
        for clause in clauses:
            if literal in clause:
                new_clauses.append([l for l in clause if l != literal])
            elif -literal in clause:
                continue
            else:
                new_clauses.append(clause + [-literal])
        return 1 + max(dpll(new_clauses, assignment + {literal: True}), dpll(new_clauses, assignment + {literal: False}))

    return dpll(cnf, {})

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    k = random.randint(1, 3)
    GF = [i for i in range(2 ** k)]
    poly = [random.choice(GF) for _ in range(n)]
    cnf = polynomial_to_cnf(poly, n)
    depth = dpll_search_tree_size(cnf)
    instances_tested = 1
    conjecture_holds = depth > n * math.log(n)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "DPLL Search Tree Depth",
        "metric_value": depth,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or generate_primes(30)
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_depth = sum(r["metric_value"] for r in results) / len(results)
    std_depth = math.sqrt(sum((r["metric_value"] - mean_depth) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_depth} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")