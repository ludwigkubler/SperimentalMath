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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        if matrix[i][i] == 0:
            raise ValueError("Singular matrix")
        for j in range(cols):
            matrix[i][j] /= matrix[i][i]
        for k in range(rows):
            if k != i and matrix[k][i] != 0:
                factor = matrix[k][i]
                for j in range(cols):
                    matrix[k][j] -= factor * matrix[i][j]

def multiply_matrices(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    if cols_A != rows_B:
        raise ValueError("Incompatible dimensions for matrix multiplication")
    result = [[sum(A[i][k] * B[k][j] for k in range(cols_A)) for j in range(cols_B)] for i in range(rows_A)]
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

def generate_random_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = random.sample(range(1, n+1), random.randint(1, n))
        clause.extend(-x for x in clause)
        cnf.append(" or ".join(f"({x})" for x in clause))
    return " and ".join(cnf)

def dual_cnf(phi):
    literals = set()
    for clause in phi.split(" and "):
        literals.update(int(x.strip("()")) for x in clause.split(" or ") if x)
    dual_clauses = []
    for literal in literals:
        dual_clause = [f"({-x})" if x == literal else f"({x})" for x in literals]
        dual_clauses.append(" or ".join(dual_clause))
    return " and ".join(dual_clauses)

def min_order(phi):
    n = len(phi.split(" and "))
    primes = [i for i in range(2, 100) if is_prime(i)]
    for p in primes:
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if i != j and (i**2 - j**2) % p == 0:
                    matrix[i][j] = 1
        try:
            gaussian_elimination(matrix)
            return len([row for row in matrix if any(x != 0 for x in row)])
        except ValueError:
            continue

def shannon_entropy(phi):
    clauses = phi.split(" and ")
    n = len(clauses)
    counts = [clauses.count(clause) for clause in set(clauses)]
    probabilities = [count / n for count in counts]
    return -sum(p * math.log2(p) for p in probabilities if p > 0)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        m = random.randint(1, n**2)
        phi = generate_random_cnf(n, m)
        phi_star = dual_cnf(phi)
        min_order_phi = min_order(phi)
        entropy_phi = shannon_entropy(phi)
        results.append((min_order_phi, entropy_phi))
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    min_order_values, entropy_values = zip(*results)
    mean_min_order = sum(min_order_values) / len(min_order_values)
    mean_entropy = sum(entropy_values) / len(entropy_values)
    std_dev = math.sqrt(sum((x - mean_min_order)**2 for x in min_order_values) / len(min_order_values))
    correlation_coefficient = sum((min_order_values[i] - mean_min_order) * (entropy_values[i] - mean_entropy) for i in range(len(min_order_values))) / (len(min_order_values) * std_dev * math.sqrt(sum((x - mean_entropy)**2 for x in entropy_values)))
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": max(5, 10, 15, 20, 30, 40),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r["metric_value"]) >= 0.7) / len(results)
    if all(abs(r["metric_value"]) >= 0.7 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev} support_fraction={support_fraction}")
    elif any(abs(r["metric_value"]) < 0.5 or abs(r["metric_value"] - (r["instances_tested"] * 2)) > 2 * std_dev for r in results):
        first_failing_seed = next((i for i, r in enumerate(results) if abs(r["metric_value"]) < 0.5 or abs(r["metric_value"] - (r["instances_tested"] * 2)) > 2 * std_dev), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")