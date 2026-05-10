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
        raise ValueError('Modular inverse does not exist')
    else:
        return x % m

def matrix_mod_inv(matrix, mod):
    n = len(matrix)
    adj = [[0 for _ in range(n)] for _ in range(n)]
    det = determinant(matrix) % mod
    if det == 0:
        raise ValueError('Matrix is not invertible')
    inv_det = mod_inverse(det, mod)
    for i in range(n):
        for j in range(n):
            minor = get_minor(matrix, i, j)
            adj[j][i] = (inv_det * determinant(minor)) % mod
    return adj

def determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    det = 0
    for c in range(len(matrix)):
        det += ((-1) ** c) * matrix[0][c] * determinant(get_minor(matrix, 0, c))
    return det

def get_minor(matrix, i, j):
    minor = []
    for r in range(len(matrix)):
        if r == i:
            continue
        row = []
        for c in range(len(matrix)):
            if c == j:
                continue
            row.append(matrix[r][c])
        minor.append(row)
    return minor

def matrix_multiply(A, B):
    n = len(A)
    m = len(B[0])
    result = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_add(A, B):
    n = len(A)
    m = len(A[0])
    result = [[A[i][j] + B[i][j] for j in range(m)] for i in range(n)]
    return result

def matrix_subtract(A, B):
    n = len(A)
    m = len(A[0])
    result = [[A[i][j] - B[i][j] for j in range(m)] for i in range(n)]
    return result

def row_reduce(matrix, mod):
    n = len(matrix)
    m = len(matrix[0])
    lead = 0
    for r in range(n):
        if lead >= m:
            break
        i = r
        while matrix[i][lead] == 0:
            i += 1
            if i == n:
                i = r
                lead += 1
                if m == lead:
                    return matrix, False
        matrix[r], matrix[i] = matrix[i], matrix[r]
        lv = matrix[r][lead]
        for j in range(m):
            matrix[r][j] = matrix[r][j] * mod_inverse(lv, mod) % mod
        for i in range(n):
            if i != r:
                cf = matrix[i][lead]
                for j in range(m):
                    matrix[i][j] = (matrix[i][j] - cf * matrix[r][j]) % mod
        lead += 1
    return matrix, True

def hilbert_function(matrix, d, mod):
    n = len(matrix)
    if d >= n:
        return 0
    A = [[matrix[i][j] for j in range(d+1)] for i in range(n)]
    B = [matrix[i][d+1] for i in range(n)]
    A_rref, reduced = row_reduce(A, mod)
    rank = sum(1 for row in A_rref if any(row[j] != 0 for j in range(len(row))))
    return n - rank

def dpll(sat_formula):
    def solve(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if solve([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if solve([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            return False
        pure_literal = next((l for l in range(1, max(abs(l) for l in set.union(*clauses)) + 1) if (l not in assignment and -l not in assignment)), None)
        if pure_literal:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            if solve([c for c in clauses if pure_literal not in c and -pure_literal not in c], new_assignment):
                return True
            new_assignment[pure_literal] = False
            if solve([c for c in clauses if pure_literal not in c and -pure_literal not in c], new_assignment):
                return True
            return False
        literal = next((l for l in range(1, max(abs(l) for l in set.union(*clauses)) + 1)), None)
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if solve([c for c in clauses if literal not in c and -literal not in c], new_assignment):
            return True
        new_assignment[literal] = False
        if solve([c for c in clauses if literal not in c and -literal not in c], new_assignment):
            return True
        return False
    return solve(sat_formula, {})

def generate_3sat_instance(n, m):
    variables = set(range(1, n + 1))
    clauses = []
    while len(clauses) < m:
        clause = random.sample(variables, 3)
        if all(l not in c and -l not in c for l in clause for c in clauses):
            clauses.append(clause)
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 3)
    sat_formula = generate_3sat_instance(n, m)
    ideal_matrix = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    for clause in sat_formula:
        for l in clause:
            for i in range(n):
                if abs(l) == i + 1:
                    ideal_matrix[i][i] += 1
    mod = 2**31 - 1
    hilbert_value = hilbert_function(ideal_matrix, n // 2, mod)
    solution_count = dpll(sat_formula)
    if solution_count == 0:
        return {
            "metric_name": "H_I(n/2)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "solution_count_zero"
        }
    conjecture_holds = abs(hilbert_value - (mod // solution_count)) < 10
    return {
        "metric_name": "H_I(n/2)",
        "metric_value": hilbert_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"solution_count={solution_count}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    mean = sum(r['metric_value'] for r in results) / len(results)
    std_dev = math.sqrt(sum((r['metric_value'] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"solution_count_zero\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")