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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_mult(A, B):
    m, n = len(A), len(B[0])
    result = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_inv(A):
    n = len(A)
    I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    for k in range(n):
        pivot = A[k][k]
        for j in range(k, n):
            A[k][j] /= pivot
            I[k][j] /= pivot
        for i in range(n):
            if i != k:
                factor = A[i][k]
                for j in range(k, n):
                    A[i][j] -= factor * A[k][j]
                    I[i][j] -= factor * I[k][j]
    return I

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        factor = A[i][i]
        for j in range(i, n):
            A[i][j] /= factor
        for j in range(n):
            if j != i:
                factor = A[j][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
    return A

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    density = 2.5
    c = 0.8
    
    def generate_3sat_instance(n, density):
        clauses = []
        for _ in range(int(density * n * (n - 1) / 6)):
            clause = [random.randint(-1, 1) * random.randint(1, n) for _ in range(3)]
            if any(abs(x) == abs(y) for x, y in zip(clause, clause[1:])):
                continue
            clauses.append(clause)
        return clauses
    
    def count_clauses(instance):
        return len(instance)
    
    def construct_number_field(m):
        m = int(m)
        discriminant = 4 * m
        if is_prime(discriminant):
            return 1
        factors = []
        for i in range(2, int(math.sqrt(discriminant)) + 1):
            while discriminant % i == 0:
                factors.append(i)
                discriminant //= i
        if discriminant > 1:
            factors.append(discriminant)
        h_K = 1
        for factor in set(factors):
            count = factors.count(factor)
            h_K *= (count + 1) // 2
        return h_K
    
    def dpll(instance):
        n = len(instance)
        clauses = [set(clause) for clause in instance]
        
        def solve(model, level):
            if not any(clause.issubset(model) for clause in clauses):
                return False
            if all(len(clause.intersection(model)) > 0 for clause in clauses):
                return True
            var = next(var for var in range(1, n + 1) if var not in model)
            pos_var = var
            neg_var = -var
            if solve(model.union({pos_var}), level + 1):
                return True
            if solve(model.union({neg_var}), level + 1):
                return True
            return False
        
        return solve(set(), 0)
    
    instance = generate_3sat_instance(n, density)
    m = count_clauses(instance)
    h_K = construct_number_field(m)
    L = dpll(instance)
    
    if L == 0:
        return {
            "metric_name": "h(K) * L / log n",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "L=0, no proof found"
        }
    
    metric_value = h_K * L / math.log(n)
    conjecture_holds = metric_value >= c
    counterexample = "" if conjecture_holds else f"m={m}, h(K)={h_K}, L={L}"
    
    return {
        "metric_name": "h(K) * L / log n",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"L=0\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data or mapping_undefined")