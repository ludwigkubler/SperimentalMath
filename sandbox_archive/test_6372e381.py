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
    return abs(a*b) // gcd(a, b)

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

def matrix_mod_inv(M, p):
    n = len(M)
    I = [[int(i == j) for j in range(n)] for i in range(n)]
    M_augmented = [row + I[i] for i, row in enumerate(M)]
    
    for i in range(n):
        pivot = M_augmented[i][i]
        if pivot == 0:
            for j in range(i+1, n):
                if M_augmented[j][i] != 0:
                    M_augmented[i], M_augmented[j] = M_augmented[j], M_augmented[i]
                    break
                else:
                    continue
            else:
                return None  # Singular matrix
        
        inv_pivot = mod_inverse(pivot, p)
        
        for j in range(n):
            M_augmented[i][j] *= inv_pivot
            M_augmented[i][j] %= p
        
        for j in range(n):
            if i != j:
                factor = M_augmented[j][i]
                for k in range(2*n):
                    M_augmented[j][k] -= factor * M_augmented[i][k]
                    M_augmented[j][k] %= p
    
    return [row[n:] for row in M_augmented]

def matrix_mod_mul(A, B, p):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
                C[i][j] %= p
    
    return C

def matrix_mod_pow(A, n, p):
    result = [[int(i == j) for j in range(len(A))] for i in range(len(A))]
    
    while n > 0:
        if n % 2 == 1:
            result = matrix_mod_mul(result, A, p)
        A = matrix_mod_mul(A, A, p)
        n //= 2
    
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
    for num in range(2, n+1):
        if is_prime(num):
            primes.append(num)
    return primes

def generate_points(n):
    points = set()
    while len(points) < n:
        point = tuple(random.randint(0, 100) for _ in range(3))
        points.add(point)
    return list(points)

def secant_variety_equations(points, p):
    n = len(points)
    equations = []
    
    for i in range(n):
        for j in range(i+1, n):
            eq = [0] * 4
            eq[0] = points[i][0] - points[j][0]
            eq[1] = points[i][1] - points[j][1]
            eq[2] = points[i][2] - points[j][2]
            eq[3] = (points[i][0]**2 + points[i][1]**2 + points[i][2]**2) % p
            equations.append(eq)
    
    return equations

def p_adic_order(equations, p):
    n = len(equations)
    M = [[0]*n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            if i == j:
                M[i][j] = 1
            else:
                M[i][j] = equations[j][i]
    
    inv_M = matrix_mod_inv(M, p)
    if inv_M is None:
        return float('inf')
    
    result = 0
    for row in inv_M:
        for val in row:
            result = max(result, math.floor(math.log2(abs(val))))
    
    return result

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        points = generate_points(n)
        equations = secant_variety_equations(points, p=101)
        order = p_adic_order(equations, p=101)
        results.append(order)
    
    mean_order = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_order)**2 for x in results) / len(results))
    
    return {
        "metric_name": "p-adic Order",
        "metric_value": mean_order,
        "instances_tested": len(n_values),
        "conjecture_holds": all(order >= n for order, n in zip(results, n_values)),
        "counterexample": "" if all(order >= n for order, n in zip(results, n_values)) else f"Order {min(order for order, n in zip(results, n_values) if order < n)} is less than n={n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean_order = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_order)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if all(order >= n for order, n in zip(r["results"], n_values))) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_dev} support_fraction={support_fraction}")
    elif any(result["conjecture_holds"] == False for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Order less than n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")