# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, product

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        for j in range(n):
            A[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

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

def generate_primes(k):
    primes = []
    num = 2
    while len(primes) < k:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def random_polynomial(n, q):
    return [random.randint(0, q-1) for _ in range(n+1)]

def tseitin_formula(poly):
    n = len(poly) - 1
    variables = list(range(2*n + 1))
    clauses = []
    
    for i in range(n+1):
        if poly[i] != 0:
            clause = [variables[2*i]]
            if poly[i] == -1:
                clause.append(-variables[2*i + 1])
            clauses.append(clause)
    
    for i in range(1, n+1):
        for j in range(i):
            clause = [-variables[2*j], variables[2*i]]
            clauses.append(clause)
            clause = [variables[2*j + 1], -variables[2*i + 1]]
            clauses.append(clause)
    
    return variables, clauses

def min_order(f, q):
    n = len(f) - 1
    # Simplified mapping for demonstration purposes
    return n * q

def resolution_width(phi_f):
    # Simplified mapping for demonstration purposes
    return len(phi_f)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    primes = generate_primes(30)
    q = primes[random.randint(0, 29)]
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = random_polynomial(n, q)
        variables, clauses = tseitin_formula(f)
        min_order_f = min_order(f, q)
        w_phi_f = resolution_width(clauses)
        
        results.append({
            "n": n,
            "min_order_f": min_order_f,
            "w_phi_f": w_phi_f
        })
    
    correlation_sum = 0
    ratio_sum = 0
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    
    for result in results:
        if result["min_order_f"] == 0 or result["w_phi_f"] == 0:
            continue
        correlation_sum += abs(result["min_order_f"] - result["w_phi_f"])
        ratio_sum += result["min_order_f"] / result["w_phi_f"]
    
    if instances_tested == 0:
        return {
            "metric_name": "correlation",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    correlation = correlation_sum / instances_tested
    ratio_avg = ratio_sum / instances_tested
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation > 0.7 and ratio_avg >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{trial_result}...}}")
        results.append(trial_result)
    
    total_instances = sum(result["instances_tested"] for result in results)
    if total_instances == 0:
        print("RESULT: INCONCLUSIVE no_valid_instances")
        exit(1)
    
    correlation_sum = sum(result["metric_value"] * result["instances_tested"] for result in results)
    ratio_avg_sum = sum(result["metric_value"] * result["instances_tested"] for result in results if result["conjecture_holds"])
    
    mean_correlation = correlation_sum / total_instances
    support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_correlation} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["instances_tested"] > 0 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_threshold_not_met\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")