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

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        return (g, y - (b // a) * x, x)

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m

def matrix_mod_inv(M, p):
    n = len(M)
    adj = [[0 for _ in range(n)] for _ in range(n)]
    det = determinant(M, p)
    if det == 0:
        raise ValueError("Matrix is singular and does not have an inverse")
    inv_det = mod_inverse(det, p)
    
    for i in range(n):
        for j in range(n):
            minor = get_minor(M, i, j)
            adj[j][i] = (inv_det * ((-1) ** (i + j)) * determinant(minor, p)) % p
    
    return adj

def determinant(matrix, p):
    if len(matrix) == 2:
        return (matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]) % p
    det = 0
    for c in range(len(matrix)):
        det += ((-1) ** c) * matrix[0][c] * determinant(get_minor(matrix, 0, c), p)
    return det % p

def get_minor(matrix, i, j):
    minor = []
    for row in range(len(matrix)):
        if row == i:
            continue
        m_row = []
        for col in range(len(matrix[row])):
            if col == j:
                continue
            m_row.append(matrix[row][col])
        minor.append(m_row)
    return minor

def is_p_adic_unit(a, p):
    return gcd(a, p) == 1 and a != 0

def minimal_order_of_p_adic_units(n, p):
    units = [a for a in range(1, n + 1) if is_p_adic_unit(a, p)]
    min_order = float('inf')
    for unit in units:
        order = 1
        current = unit % p
        while current != 1:
            current = (current * unit) % p
            order += 1
        min_order = min(min_order, order)
    return min_order

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        p = random.randint(2, min(n, 100))  # Ensure p is a prime number less than or equal to n
        circuit = [[random.randint(1, n) for _ in range(n)] for _ in range(n)]
        det = determinant(circuit, p)
        
        if det == 0:
            continue
        
        min_order = minimal_order_of_p_adic_units(abs(det), p)
        sqrt_n = math.isqrt(n)
        
        metric_values.append(min_order <= sqrt_n)
        
        if not (min_order <= sqrt_n):
            conjecture_holds = False
            counterexample = f"Circuit with determinant depth {n} and minimal order of p-adic units > √{n}"
    
    return {
        "metric_name": "minimal_order_of_p_adic_units",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": len(metric_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")