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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0]*p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    A_augmented = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A_augmented[j][i]) > abs(A_augmented[max_row][i]):
                max_row = j
        A_augmented[i], A_augmented[max_row] = A_augmented[max_row], A_augmented[i]
        pivot = A_augmented[i][i]
        for j in range(i, n+1):
            A_augmented[i][j] /= pivot
        for j in range(n):
            if i != j:
                factor = A_augmented[j][i]
                for k in range(i, n+1):
                    A_augmented[j][k] -= factor * A_augmented[i][k]
    return [row[-1] for row in A_augmented]

def is_integer_solution(A, b):
    try:
        solution = gaussian_elimination(A, b)
        for x in solution:
            if not x.denominator == 1:
                return False
        return True
    except ZeroDivisionError:
        return False

def generate_random_matrix(n):
    A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    b = [random.randint(-10, 10) for _ in range(n)]
    return A, b

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different instances
            A, b = generate_random_matrix(n)
            if is_integer_solution(A, b):
                total_metric_value += 1
            instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "integer_solution_rate",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    metric_value = total_metric_value / instances_tested
    support_fraction = metric_value >= 0.8
    
    if not support_fraction:
        counterexample = f"integer_solution_rate={metric_value:.4f}"
    
    return {
        "metric_name": "integer_solution_rate",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": support_fraction,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if "metric_value" in r)
    instances_tested = sum(r["instances_tested"] for r in results if "instances_tested" in r)
    support_fraction = sum(1 for r in results if r["conjecture_holds"])
    
    mean_metric_value = total_metric_value / len(results) if instances_tested > 0 else 0
    std_deviation = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results)) if instances_tested > 1 else 0
    
    if support_fraction >= 24:  # At least 80% seeds must support
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std={std_deviation:.4f} support_fraction={support_fraction/len(results):.2%}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"integer_solution_rate\" first_failing_seed={first_failing_seed}")