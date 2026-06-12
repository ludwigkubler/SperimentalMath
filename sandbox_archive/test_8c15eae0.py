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
        return (b, 0, 1)
    g, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return (g, x, y)

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m

def matrix_mult(A, B, mod):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
    return C

def matrix_power(A, n, mod):
    result = [[1 if i == j else 0 for j in range(len(A))] for i in range(len(A))]
    while n > 0:
        if n % 2 == 1:
            result = matrix_mult(result, A, mod)
        A = matrix_mult(A, A, mod)
        n //= 2
    return result

def p_adic_norm(poly, p):
    max_coeff = max(abs(coeff) for coeff in poly)
    return math.ceil(math.log(max_coeff, p))

def clause_indicator_poly(clause, n):
    poly = [0] * (n + 1)
    for lit in clause:
        if lit > 0:
            poly[lit - 1] += 1
        else:
            poly[-lit - 1] -= 1
    return poly

def resolution_width(clause_set):
    n = len(clause_set[0])
    clauses = list(clause_set)
    while True:
        new_clauses = set()
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                lit_i = clauses[i][0]
                lit_j = clauses[j][0]
                if -lit_i in clauses[j]:
                    new_clause = [x for x in clauses[i] if x != lit_i] + [x for x in clauses[j] if x != -lit_i and x != lit_j]
                    new_clauses.add(tuple(sorted(new_clause)))
        if len(new_clauses) == 0:
            return n
        clauses.update(new_clauses)
        n += 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    p = 2
    n_values = [5, 10, 15, 20, 30, 40]
    k_values = []
    w_values = []

    for n in n_values:
        clause_set = set()
        for _ in range(2 * n):
            clause = tuple(sorted(random.sample(range(-n, 0), 1) + random.sample(range(1, n + 1), random.randint(1, n))))
            clause_set.add(clause)
        w = resolution_width(clause_set)

        poly = [0] * (n + 1)
        for clause in clause_set:
            poly += clause_indicator_poly(clause, n)
        poly = [coeff % p for coeff in poly]

        A = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            A[i][i] = 1
        for clause in clause_set:
            if len(clause) == 2:
                lit1, lit2 = clause
                if lit1 > 0 and lit2 > 0:
                    A[lit1 - 1][lit2 - 1] += 1
                    A[lit2 - 1][lit1 - 1] += 1

        k = p_adic_norm(A, p)
        k_values.append(k)
        w_values.append(w)

    if len(k_values) < 30 or len(w_values) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(k_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }

    mean_k = sum(k_values) / len(k_values)
    mean_w = sum(w_values) / len(w_values)
    covariance = sum((k - mean_k) * (w - mean_w) for k, w in zip(k_values, w_values)) / len(k_values)
    variance_k = sum((k - mean_k) ** 2 for k in k_values) / len(k_values)
    variance_w = sum((w - mean_w) ** 2 for w in w_values) / len(w_values)
    std_dev_k = math.sqrt(variance_k)
    std_dev_w = math.sqrt(variance_w)
    correlation_coefficient = covariance / (std_dev_k * std_dev_w)

    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(k_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7 and all(correlation_coefficient >= 0.5 for _ in range(24)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and sum(1 for result in results if not result["conjecture_holds"]) < 6:
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_too_low\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data_or_unexpected_behavior")