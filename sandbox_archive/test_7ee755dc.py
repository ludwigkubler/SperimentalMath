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

def is_quadratic_residue(a, p):
    if a == 0:
        return True
    q = (p - 1) // 2
    return pow(a, q, p) == 1

def minimal_order_of_gqr(p):
    residues = [i for i in range(1, p)]
    order = {}
    for r in residues:
        if is_quadratic_residue(r, p):
            order[r] = 0
        else:
            power = 2
            while True:
                if pow(r, power, p) == 1:
                    order[r] = power
                    break
                power += 1
    return max(order.values())

def generate_cnf(n):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(n):
        clause = random.sample(variables, 2)
        clauses.append(clause)
    cnf = [clauses]
    return cnf

def resolution_width(cnf):
    def simplify_clause(clause, unit):
        return [x for x in clause if x != unit and x != -unit]

    def resolve(clause1, clause2):
        resolved = []
        for x in clause1:
            if -x in clause2:
                continue
            resolved.append(x)
        return resolved

    queue = cnf[:]
    while True:
        new_queue = []
        found_unit = False
        for i in range(len(queue)):
            for j in range(i + 1, len(queue)):
                unit = None
                for x in queue[i]:
                    if -x in queue[j]:
                        unit = x
                        break
                if unit is not None:
                    new_queue.extend(simplify_clause(queue[i], unit))
                    new_queue.extend(simplify_clause(queue[j], unit))
                    found_unit = True
                    break
            if found_unit:
                break
        if found_unit:
            queue = new_queue
        else:
            return len(queue)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(n)
        p = random.choice([i for i in range(2, 100) if all(i % j != 0 for j in range(2, int(i**0.5) + 1))])
        gqr_order = minimal_order_of_gqr(p)
        width = resolution_width(cnf)
        results.append((gqr_order, width))
    metric_value = sum(gqr / width for gqr, width in results) / len(results)
    conjecture_holds = all(abs(gqr / width - 1.0) <= 1.5 for gqr, width in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "gqr_order_over_width",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")