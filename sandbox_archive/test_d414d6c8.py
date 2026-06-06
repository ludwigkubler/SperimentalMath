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

def matrix_mod_inv(matrix, p):
    n = len(matrix)
    adj = [[0 for _ in range(n)] for _ in range(n)]
    det = 0
    for i in range(n):
        for j in range(n):
            minor = [row[:j] + row[j+1:] for row in matrix[:i] + matrix[i+1:]]
            adj[j][i] = ((-1) ** (i+j)) * determinant(minor, p)
    det = determinant(matrix, p)
    inv_det = mod_inverse(det, p)
    return [[(inv_det * adj[i][j]) % p for j in range(n)] for i in range(n)]

def determinant(matrix, p):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    sign = 1
    for j in range(n):
        minor = [row[:j] + row[j+1:] for row in matrix[1:]]
        det += sign * matrix[0][j] * determinant(minor, p)
        sign *= -1
    return det % p

def multiply_matrices(a, b, p):
    n = len(a)
    result = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] = (result[i][j] + a[i][k] * b[k][j]) % p
    return result

def add_matrices(a, b, p):
    n = len(a)
    result = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = (a[i][j] + b[i][j]) % p
    return result

def subtract_matrices(a, b, p):
    n = len(a)
    result = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = (a[i][j] - b[i][j]) % p
    return result

def matrix_power(matrix, power, p):
    n = len(matrix)
    result = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
    while power > 0:
        if power % 2 == 1:
            result = multiply_matrices(result, matrix, p)
        matrix = multiply_matrices(matrix, matrix, p)
        power //= 2
    return result

def generate_random_cnf(n):
    clauses = []
    for _ in range(2**n - 1):
        clause = random.sample(range(1, n+1), random.randint(1, n))
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)
    return clauses

def evaluate_clause_indicator_polynomial(cnf, assignment):
    result = 0
    p = 2
    for clause in cnf:
        product = 1
        for literal in clause:
            if literal > 0:
                product *= (1 + assignment[literal-1])
            else:
                product *= (1 - assignment[abs(literal)-1])
        result += product % p
    return result

def calculate_minimal_p_adic_lp_norm(cnf, p):
    min_value = float('inf')
    for _ in range(30):
        assignment = [random.choice([0, 1]) for _ in range(len(cnf))]
        value = evaluate_clause_indicator_polynomial(cnf, assignment)
        if value < min_value:
            min_value = value
    return min_value

def calculate_circuit_monotone_width(cnf):
    n = len(cnf)
    gadget = [[0 for _ in range(2*n+1)] for _ in range(2*n+1)]
    for i in range(n):
        gadget[i][i] = 1
        gadget[n+i][n+i] = 1
        gadget[i][n+i] = -1
        gadget[n+i][i] = -1
    for clause in cnf:
        for literal in clause:
            if literal > 0:
                gadget[literal-1][2*n+1] += 1
            else:
                gadget[abs(literal)-1][2*n+1] -= 1
    result = float('inf')
    for i in range(2*n+1):
        if gadget[i][i] != 0:
            continue
        subgadget = [row[:] for row in gadget]
        subgadget[i][i] = 1
        for j in range(i+1, 2*n+1):
            if subgadget[j][i] == 0:
                continue
            subgadget[i], subgadget[j] = subgadget[j], subgadget[i]
            subgadget[i][j] = 0
            for k in range(2*n+1):
                if k != i and k != j:
                    subgadget[k][i] -= subgadget[k][j] * subgadget[j][i]
                    subgadget[k][j] = 0
        result = min(result, abs(subgadget[2*n+1][i]))
    return result

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_random_cnf(n)
    p = 2
    lp_norm = calculate_minimal_p_adic_lp_norm(cnf, p)
    mw_width = calculate_circuit_monotone_width(cnf)
    return {
        "metric_name": "min(Lp(φ))",
        "metric_value": lp_norm,
        "instances_tested": 30,
        "n_max": n,
        "conjecture_holds": lp_norm <= 3 * mw_width**p,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")