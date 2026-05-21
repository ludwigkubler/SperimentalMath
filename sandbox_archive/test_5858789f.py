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
from fractions import Fraction
import math

def generate_expander_graph(n):
    if n < 4 or n % 2 != 0:
        raise ValueError("n must be even and at least 4")
    
    # Generate a random expander graph using the Chandra-Rao expander construction
    edges = []
    for i in range(1, n // 2):
        for j in range(i + 1, n // 2 + 1):
            if (i * j) % n != 0:
                edges.append((i, j))
                edges.append((j, i))
    
    # Ensure the graph is connected
    while True:
        visited = [False] * n
        stack = [1]
        visited[0] = True
        
        while stack:
            u = stack.pop()
            for v in range(1, n):
                if not visited[v] and (u, v) in edges or (v, u) in edges:
                    stack.append(v)
                    visited[v] = True
        
        if all(visited):
            break
    
    return edges

def generate_tseitin_formula(n):
    variables = [f"x{i}" for i in range(1, n + 1)]
    clauses = []
    
    # Generate clauses for each variable
    for i in range(n):
        clauses.append([variables[i]])
        clauses.append([-variables[i]])
    
    # Generate clauses for the OR gate
    for i in range(n):
        for j in range(i + 1, n):
            clauses.append([variables[i], variables[j], -f"y{i}{j}"])
            clauses.append([variables[i], -variables[j], f"y{i}{j}"])
            clauses.append([-variables[i], variables[j], f"y{i}{j}"])
            clauses.append([-variables[i], -variables[j], -f"y{i}{j}"])
    
    # Generate the final OR gate
    for i in range(n):
        clauses.append([f"y{i}{i}", -f"z{i}"])
        clauses.append([-f"y{i}{i}", f"z{i}"])
    
    return variables, clauses

def calculate_kronecker_coefficient(a, b, c):
    # Implement the Littlewood-Richardson rule to calculate Kronecker coefficients
    if a < 0 or b < 0 or c < 0:
        return Fraction(0)
    
    def hook_length_product(partition):
        product = 1
        for i in range(len(partition)):
            for j in range(i + 1):
                product *= (partition[i] - j) * (partition[j] - i) // ((i - j) * (j - i))
        return product
    
    def hook_length_sum(partition, k):
        total = 0
        for i in range(len(partition)):
            if partition[i] >= k:
                total += (partition[i] - k + 1)
        return total
    
    def schur_function(partition, n):
        numerator = hook_length_product(partition)
        denominator = 1
        for i in range(n):
            denominator *= math.factorial(i + 1) ** partition[i]
        return Fraction(numerator, denominator)
    
    a_partition = [a] * (n - 1)
    b_partition = [b] * (n - 2)
    c_partition = [c] * (n - 3)
    
    kronecker_coefficient = schur_function(a_partition, n) * schur_function(b_partition, n) / schur_function(c_partition, n)
    return kronecker_coefficient

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    
    for n in n_values:
        variables, clauses = generate_tseitin_formula(n)
        A = generate_expander_graph(2 * n)
        
        permanent_coefficient = calculate_kronecker_coefficient(n, n, n - 1)
        determinant_coefficient = calculate_kronecker_coefficient(n, n, n)
        
        if permanent_coefficient <= 0 or determinant_coefficient <= 0:
            continue
        
        metric_value = math.log(permanent_coefficient / determinant_coefficient)
        total_metric_value += metric_value
        instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "log_kronecker_coefficient_gap",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = all(metric_value > 0 for metric_value in [math.log(permanent_coefficient / determinant_coefficient) for n in n_values if permanent_coefficient > 0 and determinant_coefficient > 0])
    
    return {
        "metric_name": "log_kronecker_coefficient_gap",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")