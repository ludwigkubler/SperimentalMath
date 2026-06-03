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

def generate_kcnf(n, k):
    clauses = []
    for _ in range(k):
        clause = set()
        while len(clause) < n:
            lit = random.randint(1, n)
            if random.choice([True, False]):
                lit = -lit
            clause.add(lit)
        clauses.append(list(clause))
    return clauses

def construct_polynomials(clauses):
    polys = []
    for clause in clauses:
        poly = [1]
        for lit in clause:
            if lit > 0:
                poly = multiply_polynomials(poly, [1, -lit])
            else:
                poly = multiply_polynomials(poly, [1, lit])
        polys.append(poly)
    return polys

def multiply_polynomials(p1, p2):
    result = [0] * (len(p1) + len(p2) - 1)
    for i in range(len(p1)):
        for j in range(len(p2)):
            result[i + j] += p1[i] * p2[j]
    return [coeff % 2 for coeff in result]

def find_roots(poly):
    n = len(poly)
    if poly[-1] == 0:
        return []
    roots = []
    for i in range(1, 2**n):
        if evaluate_polynomial(poly, i) == 0:
            roots.append(i)
    return roots

def evaluate_polynomial(poly, x):
    result = 0
    power_of_x = 1
    for coeff in poly:
        result += coeff * power_of_x
        power_of_x *= x
    return result % 2

def resolution_width(cnf):
    clauses = cnf[:]
    while True:
        new_clauses = []
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                lit_i = abs(clauses[i][0])
                if -lit_i in clauses[j]:
                    new_clause = [x for x in clauses[i] if x != -lit_i]
                    new_clause.extend([x for x in clauses[j] if x != lit_i])
                    new_clauses.append(new_clause)
        if not new_clauses:
            return len(cnf) - len(clauses)
        cnf.extend(new_clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 20
    k = 5
    
    cnf = generate_kcnf(n, k)
    polys = construct_polynomials(cnf)
    
    min_root_count = float('inf')
    for poly in polys:
        roots = find_roots(poly)
        if len(roots) < min_root_count:
            min_root_count = len(roots)
    
    proof_width = resolution_width(cnf)
    
    if proof_width == 0:
        return {
            "metric_name": "alpha_over_w",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "resolution_width_zero"
        }
    
    alpha_over_w = min_root_count / proof_width
    
    return {
        "metric_name": "alpha_over_w",
        "metric_value": alpha_over_w,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": alpha_over_w <= (k * n ** (k/2 + 1)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_alpha_over_w = sum(r["metric_value"] for r in results) / len(results)
    std_alpha_over_w = math.sqrt(sum((r["metric_value"] - mean_alpha_over_w) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_alpha_over_w} std={std_alpha_over_w} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='alpha_over_w_too_large' first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown_failure_mode")