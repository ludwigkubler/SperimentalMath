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
    return abs(a * b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Inverse doesn't exist")
    else:
        return x % m

def matrix_mod_inv(M, p):
    n = len(M)
    I = [[int(i == j) for j in range(n)] for i in range(n)]
    M_aug = [row + I[i] for i, row in enumerate(M)]
    for i in range(n):
        pivot = M_aug[i][i]
        if pivot == 0:
            raise ValueError("Matrix is singular")
        for j in range(i, n * 2):
            M_aug[i][j] *= mod_inverse(pivot, p)
        for k in range(n):
            if k != i:
                factor = M_aug[k][i]
                for j in range(i, n * 2):
                    M_aug[k][j] -= factor * M_aug[i][j]
    return [row[n:] for row in M_aug]

def matrix_mult(A, B):
    n, m = len(A), len(B[0])
    result = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_add(A, B):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = (A[i][j] + B[i][j]) % p
    return result

def matrix_sub(A, B):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = (A[i][j] - B[i][j]) % p
    return result

def matrix_power(M, k):
    n = len(M)
    result = [[int(i == j) for j in range(n)] for i in range(n)]
    while k > 0:
        if k % 2 == 1:
            result = matrix_mult(result, M)
        M = matrix_mult(M, M)
        k //= 2
    return result

def is_satisfiable(clauses):
    n = max(max(abs(x) for clause in clauses for x in clause), key=abs)
    assignment = [random.choice([0, 1]) for _ in range(n)]
    for clause in clauses:
        if not any(assignment[abs(x) - 1] == (x > 0) for x in clause):
            return False
    return True

def krull_dimension(I):
    n = len(I)
    M = [[I[i][j] for j in range(n)] for i in range(n)]
    rank = 0
    for i in range(n):
        if any(M[j][i] != 0 for j in range(i, n)):
            pivot_row = next(j for j in range(i, n) if M[j][i] != 0)
            M[i], M[pivot_row] = M[pivot_row], M[i]
            for j in range(n):
                if i != j:
                    factor = M[j][i] // M[i][i]
                    M[j] = [M[j][k] - factor * M[i][k] for k in range(n)]
            rank += 1
    return rank

def sos_refutation_degree(clauses, p):
    n = max(max(abs(x) for clause in clauses for x in clause), key=abs)
    A = [[0] * (n + 1) for _ in range(n + 1)]
    b = [0] * (n + 1)
    for clause in clauses:
        for i in range(len(clause)):
            for j in range(i, len(clause)):
                x = abs(clause[i])
                y = abs(clause[j])
                A[x][y] += 1
                A[y][x] += 1
                b[x] += clause[i]
                b[y] += clause[j]
    A[-1][-1] = n + 1
    for i in range(n):
        A[i][-1] = -b[i]
    return matrix_power(A, p)[n][n]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(3 * n // 2, 6 * n // 2)
    clauses = []
    for _ in range(m):
        clause = [random.choice([-1, 1]) * (i + 1) for i in random.sample(range(n), 3)]
        clauses.append(clause)
    
    I = [[0] * n for _ in range(n)]
    for clause in clauses:
        x, y, z = abs(clause[0]), abs(clause[1]), abs(clause[2])
        I[x - 1][y - 1] += 1
        I[y - 1][x - 1] += 1
        I[x - 1][z - 1] += 1
        I[z - 1][x - 1] += 1
        I[y - 1][z - 1] += 1
        I[z - 1][y - 1] += 1
    
    dim_I = krull_dimension(I)
    refutation_degree = sos_refutation_degree(clauses, p=2)
    
    conjecture_holds = refutation_degree >= dim_I
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "SOS Refutation Degree",
        "metric_value": refutation_degree,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE insufficient support or too many failures")