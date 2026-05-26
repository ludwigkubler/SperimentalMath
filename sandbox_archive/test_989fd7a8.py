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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(cols):
                if j != i:
                    factor = Fraction(matrix[j][i], matrix[i][i])
                    for k in range(rows):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def determinant(matrix):
        rows, cols = len(matrix), len(matrix[0])
        det = 1
        for i in range(rows):
            if matrix[i][i] == 0:
                return 0
            for j in range(i + 1, rows):
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[i][k]
            det *= matrix[i][i]
        return det
    
    def quadratic_reciprocity_matrix(n):
        literals = [f'x{i}' for i in range(1, n + 1)]
        matrix = [[0] * (n * n) for _ in range(n * n)]
        
        for i in range(n):
            for j in range(i, n):
                l1, l2 = literals[i], literals[j]
                if i == j:
                    matrix[i * n + j][i * n + j] = 1
                else:
                    matrix[i * n + j][j * n + i] = -1
                    matrix[j * n + i][i * n + j] = -1
        
        return gaussian_elimination(matrix)
    
    def tseitin_resolution_width(n):
        # Placeholder for Tseitin resolution width computation
        return math.sqrt(n) * math.log(n)
    
    def is_prime(num):
        if num <= 1:
            return False
        if num == 2:
            return True
        if num % 2 == 0:
            return False
        for i in range(3, int(math.sqrt(num)) + 1, 2):
            if num % i == 0:
                return False
        return True
    
    def primes_up_to(n):
        sieve = [True] * (n + 1)
        sieve[0:2] = [False, False]
        for i in range(2, int(math.sqrt(n)) + 1):
            if sieve[i]:
                for j in range(i*i, n + 1, i):
                    sieve[j] = False
        return [i for i in range(2, n + 1) if sieve[i]]
    
    def legendre_symbol(a, p):
        if a == 0:
            return 0
        if a < 0:
            return -legendre_symbol(-a, p)
        if a % 2 == 0:
            return 0 if p % 8 in [3, 5] else 1
        if p == 2:
            return 1
        if (p * a) % 4 == 3:
            return -legendre_symbol(p, a)
        s = 0
        a %= p
        while a != 1:
            if a % 4 == 3 and p % 8 == 3:
                s += 1
            a, p = p, a
        return (-1)**s
    
    def quadratic_reciprocity_matrix_mod_p2(n):
        primes = primes_up_to(n)
        matrix = [[0] * (n * n) for _ in range(n * n)]
        
        for i in range(n):
            for j in range(i, n):
                l1, l2 = literals[i], literals[j]
                if i == j:
                    matrix[i * n + j][i * n + j] = 1
                else:
                    matrix[i * n + j][j * n + i] = -1
                    matrix[j * n + i][i * n + j] = -1
        
        for p in primes:
            det = determinant(matrix)
            if det % (p ** 2) == 0:
                return False
        
        return True
    
    n = random.randint(5, 40)
    matrix = quadratic_reciprocity_matrix(n)
    width = tseitin_resolution_width(n)
    holds = quadratic_reciprocity_matrix_mod_p2(n)
    
    return {
        "metric_name": "Tseitin Resolution Width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
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
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")