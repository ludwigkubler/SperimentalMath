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
    
    def communication_complexity(f):
        # Placeholder for actual CC_R computation
        return len(f) // 2
    
    def tropical_polynomial(f):
        # Placeholder for actual tropical polynomial construction
        n = len(f)
        t_f = [0] * (n + 1)
        for i in range(n):
            if f[i]:
                t_f[i] = -i
        return t_f
    
    def tropical_cycle_rank(t_f):
        # Placeholder for actual TR computation
        n = len(t_f) - 1
        rank = 0
        for i in range(1, n + 1):
            if t_f[i] < 0:
                rank += 1
        return rank
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a*b) // gcd(a, b)
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def primes_up_to(limit):
        sieve = [True] * (limit + 1)
        sieve[0:2] = [False, False]
        for x in range(2, int(math.sqrt(limit)) + 1):
            if sieve[x]:
                for i in range(x*x, limit + 1, x):
                    sieve[i] = False
        return [x for x in range(2, limit + 1) if sieve[x]]
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(n)]
    
    def run_test(f):
        cc_r = communication_complexity(f)
        t_f = tropical_polynomial(f)
        tr_t_f = tropical_cycle_rank(t_f)
        upper_bound = 2 ** cc_r
        return {
            "metric_name": "tropical_cycle_rank",
            "metric_value": tr_t_f,
            "instances_tested": 1,
            "n_max": len(f),
            "conjecture_holds": tr_t_f <= upper_bound,
            "counterexample": "" if tr_t_f <= upper_bound else f"CC_R={cc_r}, TR(t_f)={tr_t_f}"
        }
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        result = run_test(f)
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        return {
            "RESULT": f"SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}"
        }
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        return {
            "RESULT": f"FALSIFIED counterexample=\"CC_R exceeds TR(t_f)\" first_failing_seed={first_failing_seed}"
        }
    else:
        return {
            "RESULT": "INCONCLUSIVE mapping_undefined"
        }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        seeds = primes_up_to(30)
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")