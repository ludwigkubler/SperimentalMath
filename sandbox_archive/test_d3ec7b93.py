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

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a * b) // gcd(a, b)
    
    def extended_gcd(a, b):
        if a == 0:
            return (b, 0, 1)
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
    
    def matrix_mod_inv(matrix, mod):
        n = len(matrix)
        det = 0
        for i in range(n):
            det += matrix[0][i] * matrix_minor(matrix, 0, i) * (-1) ** (0 + i)
        det = det % mod
        inv_det = mod_inverse(det, mod)
        adjugate = []
        for i in range(n):
            row = []
            for j in range(n):
                minor = matrix_minor(matrix, i, j)
                cofactor = (-1) ** (i + j) * minor
                row.append(cofactor % mod)
            adjugate.append(row)
        inv_matrix = [[(adjugate[j][i] * inv_det) % mod for i in range(n)] for j in range(n)]
        return inv_matrix
    
    def matrix_minor(matrix, i, j):
        submatrix = []
        for r in range(len(matrix)):
            if r != i:
                row = []
                for c in range(len(matrix[r])):
                    if c != j:
                        row.append(matrix[r][c])
                submatrix.append(row)
        return determinant(submatrix)
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for i in range(n):
            det += matrix[0][i] * determinant([[matrix[j][k] for k in range(i, n)] for j in range(1, n)]) * (-1) ** (0 + i)
        return det
    
    def matrix_mult(A, B, mod):
        result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
        for i in range(len(A)):
            for j in range(len(B[0])):
                for k in range(len(B)):
                    result[i][j] = (result[i][j] + A[i][k] * B[k][j]) % mod
        return result
    
    def matrix_add(A, B, mod):
        result = [[(A[i][j] + B[i][j]) % mod for j in range(len(B[0]))] for i in range(len(A))]
        return result
    
    def matrix_sub(A, B, mod):
        result = [[(A[i][j] - B[i][j]) % mod for j in range(len(B[0]))] for i in range(len(A))]
        return result
    
    def matrix_pow(matrix, n, mod):
        if n == 1:
            return matrix
        elif n % 2 == 0:
            half = matrix_pow(matrix, n // 2, mod)
            return matrix_mult(half, half, mod)
        else:
            return matrix_mult(matrix, matrix_pow(matrix, n - 1, mod), mod)
    
    def is_invertible(matrix):
        det = determinant(matrix)
        return det != 0
    
    def gaussian_elimination(A, b, mod):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            pivot = A[i][i]
            for j in range(i, n):
                A[i][j] = (A[i][j] * mod_inverse(pivot, mod)) % mod
            b[i] = (b[i] * mod_inverse(pivot, mod)) % mod
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(i, n):
                        A[j][k] = (A[j][k] - factor * A[i][k]) % mod
                    b[j] = (b[j] - factor * b[i]) % mod
        return A, b
    
    def solve_linear_system(A, b, mod):
        A, b = gaussian_elimination(A, b, mod)
        n = len(A)
        x = [0 for _ in range(n)]
        for i in range(n - 1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) % mod
        return x
    
    def matrix_rank(matrix):
        A = [row[:] for row in matrix]
        rank = 0
        for i in range(len(A)):
            if A[i]:
                rank += 1
                for j in range(i + 1, len(A)):
                    factor = A[j][i] / A[i][i]
                    A[j] = [A[j][k] - factor * A[i][k] for k in range(len(A[0]))]
        return rank
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 ** n):
            clause = []
            for i in range(n):
                if random.choice([True, False]):
                    clause.append(random.choice([-1, 1]) * (i + 1))
            if len(clause) > 0:
                clauses.append(clause)
        return clauses
    
    def generate_matrix_from_clauses(clauses, n):
        m = len(clauses)
        A = [[0 for _ in range(n)] for _ in range(m)]
        b = [0 for _ in range(m)]
        for i, clause in enumerate(clauses):
            for var in clause:
                if var > 0:
                    A[i][var - 1] += 1
                else:
                    A[i][-var - 1] -= 1
            b[i] = 1
        return A, b
    
    def find_irreducible_components(A, b, mod):
        rank_A = matrix_rank(A)
        rank_AB = matrix_rank(matrix_add(A, [[0 for _ in range(len(b))] + [b]], mod))
        irreducible_components = rank_AB - rank_A
        return irreducible_components
    
    n = 40
    s_F = random.randint(10, 100)  # Minimal circuit size (simplified)
    
    clauses = generate_3cnf(n)
    A, b = generate_matrix_from_clauses(clauses, n)
    
    try:
        irreducible_components = find_irreducible_components(A, b, mod=2 ** 64 - 1)
        log_s_F = math.log(s_F, 2)
        
        metric_name = "Irreducible Component Count"
        metric_value = irreducible_components
        instances_tested = 1
        conjecture_holds = abs(irreducible_components - log_s_F) < 0.5 * log_s_F
        counterexample = "" if conjecture_holds else f"Counterexample: {irreducible_components} != {log_s_F}"
        
        return {
            "metric_name": metric_name,
            "metric_value": metric_value,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }
    except Exception as e:
        print(f"Error in run_trial(seed={seed}): {e}")
        return {
            "metric_name": "",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": str(e)
        }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(arg) for arg in sys.argv[1:]]
    else:
        primes = generate_primes(30)
        seeds = primes[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")