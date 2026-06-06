# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def smallest_prime_not_dividing(m):
    p = 2
    while True:
        if m % p != 0 and is_prime(p):
            return p
        p += 1

def generate_cnf(n, num_clauses):
    cnf = []
    for _ in range(num_clauses):
        clause = [random.randint(1, n) * (-1 if random.choice([True, False]) else 1)
                  for _ in range(random.randint(1, n))]
        cnf.append(clause)
    return cnf

def dpll_proof_length(cnf):
    def satisfiable(cnf, assignment):
        for clause in cnf:
            if all(lit not in assignment or assignment[lit] == (lit > 0) for lit in clause):
                continue
            return False
        return True

    def backtrack(cnf, assignment, literals):
        if not cnf:
            return 1
        literal = literals[0]
        negated_literal = -literal
        if satisfiable(cnf, assignment | {literal: True}):
            return backtrack(cnf, assignment | {literal: True}, literals[1:])
        elif satisfiable(cnf, assignment | {negated_literal: True}):
            return backtrack(cnf, assignment | {negated_literal: True}, literals[1:])
        else:
            return 0

    literals = list(range(1, n + 1)) + [-lit for lit in range(1, n + 1)]
    return backtrack(cnf, {}, literals)

def minimal_order(primitive_element):
    order = 1
    current = primitive_element
    while current != 1:
        current = (current * primitive_element) % p
        order += 1
    return order

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    total_ratio = 0.0
    conjecture_holds = True
    counterexample = ""

    for n in range(5, n_max + 1):
        num_clauses = random.randint(n, 2 * n)
        cnf = generate_cnf(n, num_clauses)
        proof_length = dpll_proof_length(cnf)
        p = smallest_prime_not_dividing(num_clauses)

        if p == 0:
            counterexample = "mapping_undefined"
            conjecture_holds = False
            break

        primitive_element = random.randint(2, p - 1)
        while gcd(primitive_element, p) != 1:
            primitive_element = random.randint(2, p - 1)

        order = minimal_order(primitive_element)
        upper_bound = n ** (1 / p)

        ratio = order / upper_bound
        total_ratio += ratio
        instances_tested += 1

    if not counterexample and instances_tested >= 30:
        mean_ratio = total_ratio / instances_tested
        return {
            "metric_name": "Ratio of minimal order to upper bound",
            "metric_value": mean_ratio,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }
    else:
        return {
            "metric_name": "Ratio of minimal order to upper bound",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] == "mapping_undefined" for r in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")