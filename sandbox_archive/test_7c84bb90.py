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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_random_cnf(n, num_clauses):
    clauses = []
    variables = list(range(1, n + 1))
    for _ in range(num_clauses):
        clause = random.sample(variables, random.randint(1, n))
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)
    return clauses

def characteristic_polynomial(cnf):
    n = len(cnf[0])
    p = [1] + [0] * (n - 1)
    for clause in cnf:
        coeff = 1
        for var in clause:
            if var > 0:
                coeff *= (1 - x[var - 1])
            else:
                coeff *= (1 + x[-var - 1])
        p = [p[i] * coeff for i in range(n)]
    return p

def min_non_zero_coeff(p):
    for coeff in p:
        if coeff != 0:
            return abs(coeff)
    return None

def resolution_width(cnf):
    clauses = set(tuple(sorted(clause)) for clause in cnf)
    queue = list(clauses)
    while queue:
        clause1 = queue.pop()
        for clause2 in queue:
            new_clause = []
            for lit1 in clause1:
                if -lit1 in clause2:
                    continue
                new_clause.append(lit1)
            if not new_clause:
                return len(queue) + 1
            new_clause = tuple(sorted(new_clause))
            if new_clause not in queue and new_clause not in clauses:
                queue.append(new_clause)
    return len(queue)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for n in range(5, n_max + 1):
        if n % 2 == 0:
            continue
        p = random.randint(3, 100)
        while gcd(p, math.factorial(n)) != 1 or not is_prime(p):
            p = random.randint(3, 100)

        cnf = generate_random_cnf(n, n * (n - 1) // 2)
        x = [random.choice([1, -1]) for _ in range(n)]
        p = characteristic_polynomial(cnf)
        k = min_non_zero_coeff(p)
        if k is None:
            conjecture_holds = False
            counterexample = "mapping_undefined"
            break

        w = resolution_width(cnf)
        instances_tested += 1
        total_metric_value += w / (k ** 2 * math.log(n))
        if w < k ** 2 * math.log(n):
            conjecture_holds = False
            counterexample = f"n={n}, k={k}, w={w}"
            break

    return {
        "metric_name": "resolution_width",
        "metric_value": total_metric_value / instances_tested if instances_tested > 0 else None,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)

    total_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    instances_tested = sum(r["instances_tested"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value / instances_tested} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")