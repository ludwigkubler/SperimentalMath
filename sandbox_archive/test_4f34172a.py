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

def primes(n):
    sieve = [True] * (n+1)
    p = 2
    while (p * p <= n):
        if (sieve[p] == True):
            for i in range(p * p, n+1, p):
                sieve[i] = False
        p += 1
    return [p for p in range(2, n)]

def random_sat_instance(n: int) -> list:
    clauses = []
    variables = set()
    for _ in range(n):
        clause = []
        for _ in range(random.randint(1, n)):
            var = random.choice(list(variables)) if variables else f'v{random.randint(1, 2*n)}'
            variables.add(var)
            clause.append((var, random.choice([True, False])))
        clauses.append(clause)
    return clauses

def indicator_polynomial(cnf: list) -> dict:
    poly = {}
    for clause in cnf:
        term = 1
        for var, sign in clause:
            if sign:
                term *= (1 + int(var[1:]) if var.startswith('v') else -int(var[1:]))
            else:
                term *= (-1 + int(var[1:]) if var.startswith('v') else 1 - int(var[1:]))
        poly[tuple(sorted(clause))] = term
    return poly

def tropical_add(x, y):
    return max(x, y)

def tropical_multiply(x, y):
    return x + y

def tropical_abelianization(poly: dict) -> int:
    order = 0
    for clause in poly:
        term_order = sum(1 for var, _ in clause)
        if term_order > order:
            order = term_order
    return order

def dpll(cnf: list, assignment: dict = {}) -> bool:
    if not cnf:
        return True
    literal = next((l for l in cnf[0] if l[1]), None)
    if literal is None:
        return False
    var, sign = literal
    new_assignment = assignment.copy()
    new_assignment[var] = sign
    if dpll([c for c in cnf if not any(l == (var, s) for l, s in c)], new_assignment):
        return True
    new_assignment[var] = not sign
    return dpll([c for c in cnf if not any(l == (var, s) for l, s in c)], new_assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = random_sat_instance(n)
            poly = indicator_polynomial(cnf)
            ord_ab = tropical_abelianization(poly)
            proof_length = len(dpll(cnf))
            metric_values.append((ord_ab, proof_length))
            instances_tested += 1
            if ord_ab != proof_length:
                conjecture_holds = False
                counterexample = f"n={n}, ord_ab={ord_ab}, proof_length={proof_length}"
                break

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": sum(x * y for x, y in metric_values) / (sum(x**2 for x, _ in metric_values) * sum(y**2 for _, y in metric_values)) ** 0.5,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else primes(30)
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")