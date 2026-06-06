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
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m

def matrix_mul(A, B, mod):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
                result[i][j] %= mod
    return result

def matrix_pow(A, n, mod):
    result = [[0 if i != j else 1 for j in range(len(A))] for i in range(len(A))]
    while n > 0:
        if n % 2 == 1:
            result = matrix_mul(result, A, mod)
        A = matrix_mul(A, A, mod)
        n //= 2
    return result

def indicator_polynomial(cnf):
    n = len(cnf)
    poly = [0] * (n + 1)
    poly[0] = 1
    for clause in cnf:
        term = 1
        for literal in clause:
            term *= -poly[-literal]
            term %= 2
        poly[0] += term
        poly[0] %= 2
    return poly

def tropical_abelianization(poly):
    n = len(poly)
    abelianization = [0] * (n + 1)
    for i in range(n, -1, -1):
        if poly[i] != 0:
            abelianization[i] = i
            break
    return abelianization

def dpll(cnf, assignment=None):
    if assignment is None:
        assignment = [False] * len(cnf)
    n = len(cnf)
    for i in range(n):
        if not assignment[i]:
            new_assignment = assignment[:]
            new_assignment[i] = True
            if dpll(cnf, new_assignment):
                return True
            new_assignment[i] = False
            if dpll(cnf, new_assignment):
                return True
            return False
    for clause in cnf:
        if all(not literal in assignment or not assignment[literal] for literal in clause):
            return False
    return True

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = [[random.randint(1, n) for _ in range(random.randint(1, 3))] for _ in range(n)]
        poly = indicator_polynomial(cnf)
        abelianization = tropical_abelianization(poly)
        ord_ab = abelianization[0]
        proof_length = len(dpll(cnf)) if dpll(cnf) else float('inf')
        results.append((ord_ab, proof_length))
    instances_tested = len(results)
    n_max = max(n_values)
    metric_name = "correlation_coefficient"
    metric_value = sum(x * y for x, y in results) / (sum(x**2 for x, _ in results) * sum(y**2 for _, y in results))**0.5
    conjecture_holds = metric_value >= 0.7
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
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
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")