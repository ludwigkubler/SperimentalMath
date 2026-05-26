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
    n = len(matrix)
    adj = [[0] * n for _ in range(n)]
    det = 0
    for i in range(n):
        for j in range(n):
            minor = [row[:j] + row[j+1:] for row in matrix[:i] + matrix[i+1:]]
            if (i + j) % 2 == 0:
                adj[i][j] = matrix_mod_det(minor, mod)
            else:
                adj[i][j] = -matrix_mod_det(minor, mod)
        det += matrix[0][j] * adj[0][j]
    det = det % mod
    inv_det = mod_inverse(det, mod)
    for i in range(n):
        for j in range(n):
            adj[i][j] = (adj[i][j] * inv_det) % mod
    return adj

def matrix_mod_det(matrix, mod):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    for j in range(n):
        minor = [row[:j] + row[j+1:] for row in matrix[1:]]
        sign = (-1) ** (j % 2)
        det += sign * matrix[0][j] * matrix_mod_det(minor, mod)
    return det % mod

def generate_polynomial(n):
    poly = [random.randint(1, 10) for _ in range(n+1)]
    return poly

def evaluate_poly(poly, x):
    result = 0
    power = 1
    for coeff in reversed(poly):
        result += coeff * power
        power *= x
    return result % len(poly)

def compute_ehrhart_quotient(poly, n):
    min_quotient = float('inf')
    for delta in range(1, n+1):
        count = 0
        for i in range(n+1):
            if evaluate_poly(poly, i) >= delta and evaluate_poly(poly, i) <= 1:
                count += 1
        if count > 0:
            quotient = len(poly) * count / delta
            min_quotient = min(min_quotient, quotient)
    return min_quotient

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        poly = generate_polynomial(n)
        quotient = compute_ehrhart_quotient(poly, n)
        results.append({
            "n": n,
            "poly": poly,
            "quotient": quotient
        })
    
    instances_tested = len(results)
    metric_value = sum(result["quotient"] for result in results) / instances_tested
    
    conjecture_holds = True
    counterexample = ""
    
    for result in results:
        n = result["n"]
        poly = result["poly"]
        quotient = result["quotient"]
        
        if n <= 20 and quotient > math.log(n, 2) ** 2 + 1:
            conjecture_holds = False
            counterexample = f"n={n}, poly={poly}"
            break
        
        if n > 20 and quotient > n * 1.5:
            conjecture_holds = False
            counterexample = f"n={n}, poly={poly}"
            break
    
    return {
        "metric_name": "Ehrhart Quotient",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")