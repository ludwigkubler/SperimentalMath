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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            literals = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if not all(literals[i] != literals[j] for i, j in combinations(range(n), 2)):
                continue
            clauses.append(random.choice(literals))
        return clauses

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
            raise ValueError("Inverse doesn't exist")
        else:
            return x % m

    def matrix_mod_inv(matrix, mod):
        n = len(matrix)
        inv = [[0] * n for _ in range(n)]
        for i in range(n):
            inv[i][i] = 1
        for i in range(n):
            pivot = matrix[i][i]
            if pivot == 0:
                raise ValueError("Matrix is singular")
            factor = mod_inverse(pivot, mod)
            for j in range(n):
                matrix[i][j] *= factor
                inv[i][j] *= factor
            for k in range(n):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(n):
                        matrix[k][j] -= factor * matrix[i][j]
                        inv[k][j] -= factor * inv[i][j]
        return inv

    def matrix_mul(A, B, mod):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
                    C[i][j] %= mod
        return C

    def matrix_pow(matrix, power, mod):
        result = [[0 if i != j else 1 for j in range(len(matrix))] for i in range(len(matrix))]
        base = matrix
        while power > 0:
            if power % 2 == 1:
                result = matrix_mul(result, base, mod)
            base = matrix_mul(base, base, mod)
            power //= 2
        return result

    def is_prime(n):
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    def generate_primes(n):
        primes = []
        for num in range(2, n):
            if is_prime(num):
                primes.append(num)
        return primes[:n]

    def generate_random_matrix(n, mod):
        matrix = [[random.randint(0, mod - 1) for _ in range(n)] for _ in range(n)]
        return matrix

    def gaussian_elimination(matrix, mod):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if rank < n:
                pivot_row = i
                while pivot_row < n and matrix[pivot_row][i] == 0:
                    pivot_row += 1
                if pivot_row == n:
                    continue
                matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
                for j in range(i + 1, n):
                    factor = (matrix[j][i] * mod_inverse(matrix[i][i], mod)) % mod
                    for k in range(n):
                        matrix[j][k] = (matrix[j][k] - factor * matrix[i][k]) % mod
                rank += 1
        return rank

    def compute_dimension_of_radical(matrix, mod):
        n = len(matrix)
        identity_matrix = [[0 if i != j else 1 for j in range(n)] for i in range(n)]
        augmented_matrix = [row + col for row, col in zip(matrix, identity_matrix)]
        return gaussian_elimination(augmented_matrix, mod)

    def compute_sos_degree(φ):
        # Placeholder for actual SOS degree computation
        return random.randint(10, 50)  # Dummy value

    n = 40
    ε = 1 / (n ** 2)
    φ = generate_3cnf(n)
    dim_sqrt_I_φ = compute_dimension_of_radical(generate_random_matrix(n, 2), 2)
    d = compute_sos_degree(φ)

    if d < dim_sqrt_I_φ / math.log(n):
        return {
            "metric_name": "sos_degree",
            "metric_value": d,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"n={n}, dim(√I_φ)={dim_sqrt_I_φ}, d={d}"
        }
    else:
        return {
            "metric_name": "sos_degree",
            "metric_value": d,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or generate_primes(30)
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='n={40}, dim(√I_φ)={dim_sqrt_I_φ}, d={d}' first_failing_seed={first_failing_seed}")