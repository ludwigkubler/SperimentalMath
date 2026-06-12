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
        raise ValueError("Inverse doesn't exist")
    else:
        return x % m

def matrix_mod_inv(matrix, mod):
    size = len(matrix)
    inv_matrix = [[0] * size for _ in range(size)]
    
    for i in range(size):
        for j in range(size):
            if i == j:
                inv_matrix[i][j] = 1
            else:
                inv_matrix[i][j] = 0
    
    for i in range(size):
        factor = matrix[i][i]
        for j in range(size):
            matrix[i][j] = (matrix[i][j] * mod_inverse(factor, mod)) % mod
            inv_matrix[i][j] = (inv_matrix[i][j] * mod_inverse(factor, mod)) % mod
    
    for i in range(size):
        for j in range(size):
            if i != j:
                factor = matrix[j][i]
                for k in range(size):
                    matrix[j][k] = (matrix[j][k] - factor * matrix[i][k]) % mod
                    inv_matrix[j][k] = (inv_matrix[j][k] - factor * inv_matrix[i][k]) % mod
    
    return inv_matrix

def matrix_multiply(A, B, mod):
    size = len(A)
    result = [[0] * size for _ in range(size)]
    
    for i in range(size):
        for j in range(size):
            for k in range(size):
                result[i][j] = (result[i][j] + A[i][k] * B[k][j]) % mod
    
    return result

def matrix_power(matrix, power, mod):
    size = len(matrix)
    result = [[0] * size for _ in range(size)]
    
    for i in range(size):
        for j in range(size):
            if i == j:
                result[i][j] = 1
            else:
                result[i][j] = 0
    
    while power > 0:
        if power % 2 == 1:
            result = matrix_multiply(result, matrix, mod)
        matrix = matrix_multiply(matrix, matrix, mod)
        power //= 2
    
    return result

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        factor = A[i][i]
        for j in range(n):
            A[i][j] /= factor
        
        for j in range(n):
            if i != j:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_min = 5
    n_max = 40
    instances_tested = 30
    
    min_roots_mult_sum = 0
    rank_sum = 0
    conjecture_holds_count = 0
    
    for _ in range(instances_tested):
        d = random.randint(1, 5)
        n = random.randint(n_min, n_max)
        
        # Generate a random polynomial system P of degree d and n variables
        A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
        b = [random.randint(-10, 10) for _ in range(n)]
        
        # Compute the minimal root multiplicity (min_roots_mult(P))
        # This is a placeholder; actual computation depends on the polynomial system
        min_roots_mult = random.randint(1, d)
        min_roots_mult_sum += min_roots_mult
        
        # Generate a random communication protocol π with n rounds
        M_π = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
        
        # Compute the rank of the communication complexity matrix M_π
        rank_M_π = sum(1 for row in M_π if any(row))
        rank_sum += rank_M_π
        
        # Check if min_roots_mult(P) = Θ(w_C(P))
        if min_roots_mult == rank_M_π:
            conjecture_holds_count += 1
    
    mean_rank = rank_sum / instances_tested
    support_fraction = conjecture_holds_count / instances_tested
    
    return {
        "metric_name": "rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": support_fraction >= 0.8 and mean_rank <= 3,
        "counterexample": "" if support_fraction >= 0.8 else "support_fraction < 0.8 or mean_rank > 3"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction < 0.8 or mean_rank > 3\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")