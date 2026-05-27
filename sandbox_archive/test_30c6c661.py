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
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = 1 / A[i][i]
            for j in range(n):
                if i != j:
                    A[j][i] /= factor
            b[i] /= factor
            for j in range(i + 1, n):
                factor = A[j][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        return [b[i] / A[i][i] for i in range(n)]
    
    def matrix_multiply(A, B):
        m = len(A)
        p = len(B[0])
        q = len(B)
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(q):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def is_prime(n):
        if n <= 1:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    def generate_primes(n):
        primes = []
        for num in range(2, n * n):
            if is_prime(num) and len(primes) < n:
                primes.append(num)
        return primes
    
    def tseitin_circuit(w, n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clauses.append([variables[i]])
        for i in range(1, w + 1):
            new_var = f'y{i}'
            clauses.append([new_var])
            for j in range(i):
                clauses.append([-clauses[j][-1], -new_var, variables[j]])
        return variables, clauses
    
    def compute_symmetry_group(clauses):
        # Simplified symmetry group computation
        symmetries = []
        n = len(clauses)
        for perm in itertools.permutations(range(n)):
            if all(clauses[perm[i]] == clauses[i] for i in range(n)):
                symmetries.append(perm)
        return symmetries
    
    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(len(x))) / len(x))
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(len(y))) / len(y))
        return cov_xy / (std_x * std_y)
    
    def run_trial(seed: int) -> dict:
        random.seed(seed)
        
        n = random.randint(5, 40)
        w = random.randint(1, n // 2)
        variables, clauses = tseitin_circuit(w, n)
        symmetries = compute_symmetry_group(clauses)
        S_f = len(symmetries)
        
        if S_f == 0:
            return {
                "metric_name": "S(f)",
                "metric_value": S_f,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        c = random.uniform(0.5, 2.0)
        cw = c * w
        
        return {
            "metric_name": "S(f)",
            "metric_value": S_f,
            "instances_tested": 1,
            "conjecture_holds": S_f <= cw,
            "counterexample": ""
        }
    
    seeds = generate_primes(30)
    results = []
    for seed in seeds:
        result = run_trial(seed)
        results.append(result)
        print(f"TRIAL: {result}")
    
    mean_S_f = sum(r["metric_value"] for r in results) / len(results)
    std_S_f = math.sqrt(sum((r["metric_value"] - mean_S_f) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_S_f} std={std_S_f} support_fraction={support_fraction}")
    elif support_fraction < 0.3:
        counterexample = "first failing seed"
        for i, r in enumerate(results):
            if not r["conjecture_holds"]:
                counterexample += f" {i+1}"
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[i]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")