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

def matrix_mod_inv(matrix, m):
    n = len(matrix)
    adj = [[0 for _ in range(n)] for _ in range(n)]
    det = determinant(matrix, m)
    if det == 0:
        raise ValueError("Matrix is singular and does not have an inverse")
    inv_det = mod_inverse(det, m)
    
    for i in range(n):
        for j in range(n):
            minor = get_minor(matrix, i, j)
            adj[j][i] = (inv_det * (-1) ** (i + j)) % m
    
    return adj

def determinant(matrix, m):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    
    det = 0
    for i in range(n):
        minor = get_minor(matrix, 0, i)
        det += ((-1) ** i) * matrix[0][i] * determinant(minor, m)
    
    return det % m

def get_minor(matrix, row, col):
    n = len(matrix)
    minor = []
    for r in range(n):
        if r == row:
            continue
        new_row = []
        for c in range(n):
            if c == col:
                continue
            new_row.append(matrix[r][c])
        minor.append(new_row)
    
    return minor

def matrix_mul(A, B, m):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % m
    
    return C

def matrix_add(A, B, m):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = (A[i][j] + B[i][j]) % m
    
    return C

def matrix_sub(A, B, m):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = (A[i][j] - B[i][j]) % m
    
    return C

def matrix_pow(matrix, n, m):
    result = [[0 for _ in range(len(matrix))] for _ in range(len(matrix))]
    for i in range(len(matrix)):
        result[i][i] = 1
    
    while n > 0:
        if n % 2 == 1:
            result = matrix_mul(result, matrix, m)
        matrix = matrix_mul(matrix, matrix, m)
        n //= 2
    
    return result

def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def generate_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    
    return primes

def random_cnf(n, m):
    clauses = []
    for _ in range(m):
        clause = [random.randint(1, n), random.randint(-n, -1)]
        clauses.append(clause)
    
    return clauses

def dpll_solver(cnf):
    def solve(model):
        if not cnf:
            return True
        literal = next((l for l in model if l > 0), None)
        if literal is None:
            return False
        
        new_model = model[:]
        new_model.append(literal)
        if solve(new_model):
            return True
        
        new_model.pop()
        new_model.append(-literal)
        if solve(new_model):
            return True
        
        return False
    
    return solve([])

def min_rank(cnf, m):
    n = len(cnf[0])
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    
    for clause in cnf:
        for literal in clause:
            row = abs(literal) - 1
            col = literal > 0
    
    rank = 0
    while True:
        pivot_row = next((i for i in range(rank, n) if matrix[i][rank] != 0), None)
        if pivot_row is None:
            break
        
        for j in range(n):
            matrix[pivot_row][j], matrix[rank][j] = matrix[rank][j], matrix[pivot_row][j]
        
        for i in range(n):
            if i == rank:
                continue
            factor = matrix[i][rank] // matrix[rank][rank]
            for j in range(n):
                matrix[i][j] -= factor * matrix[rank][j]
        
        rank += 1
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = random_cnf(n, n * (n - 1) // 2)
        rank = min_rank(cnf, 2**63 - 1)
        width = dpll_solver(cnf)
        
        if rank == 0 or width == 0:
            continue
        
        results.append((rank, width))
    
    if not results:
        return {
            "metric_name": "min_rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ranks = [r for r, w in results]
    widths = [w for r, w in results]
    
    mean_rank = sum(ranks) / len(ranks)
    mean_width = sum(widths) / len(widths)
    
    correlation = 0
    n = len(results)
    if n > 1:
        numerator = sum((r - mean_rank) * (w - mean_width) for r, w in results)
        denominator = math.sqrt(sum((r - mean_rank) ** 2 for r, _ in results)) * math.sqrt(sum((w - mean_width) ** 2 for _, w in results))
        correlation = numerator / denominator
    
    return {
        "metric_name": "min_rank",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}"
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result = f"FALSIFIED counterexample='' first_failing_seed={first_failing_seed}"
    else:
        result = "INCONCLUSIVE reason=unknown"
    
    print(result)