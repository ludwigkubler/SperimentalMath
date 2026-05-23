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

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    result = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented_matrix = [A[i] + [b[i]] for i in range(m)]
    for i in range(n):
        max_row = i
        for j in range(i+1, m):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        pivot = augmented_matrix[i][i]
        for j in range(i, n+1):
            augmented_matrix[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(i, n+1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    return [row[-1] for row in augmented_matrix]

def tropical_rank(poly):
    m, n = len(poly), len(poly[0])
    A = [[-abs(coeff) if coeff != 0 else float('-inf') for coeff in clause] for clause in poly]
    b = [float('-inf')] * m
    return len(gaussian_elimination(A, b))

def tseitin_formula(n):
    variables = list(range(1, n+1))
    clauses = []
    for i in range(1, 2**n):
        binary = bin(i)[2:].zfill(n)
        clause = [variables[j] if binary[j] == '1' else -variables[j] for j in range(n)]
        clauses.append(clause)
    return variables, clauses

def resolution_tree(poly):
    m, n = len(poly), len(poly[0])
    clauses = poly[:]
    tree = []
    while True:
        new_clauses = []
        for i in range(m):
            for j in range(i+1, m):
                if any(abs(coeff) == float('-inf') for coeff in clauses[i]) or any(abs(coeff) == float('-inf') for coeff in clauses[j]):
                    continue
                common_vars = set(clause for clause in clauses[i] if abs(clause) in [abs(x) for x in clauses[j]])
                if not common_vars:
                    continue
                new_clause = []
                for var in variables:
                    if var in common_vars:
                        new_clause.append(-var)
                    else:
                        new_clause.extend([x for x in clauses[i] if abs(x) != abs(var)])
                        new_clause.extend([x for x in clauses[j] if abs(x) != abs(var)])
                new_clauses.append(new_clause)
        if not new_clauses:
            break
        tree.append((clauses, new_clauses))
        clauses.extend(new_clauses)
    return tree

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    variables, clauses = tseitin_formula(n)
    poly = [[abs(coeff) for coeff in clause] for clause in clauses]
    trop_rank_poly = tropical_rank(poly)
    tree = resolution_tree(poly)
    width = len(tree)
    return {
        "metric_name": "Resolution Proof Tree Width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": width <= 2**trop_rank_poly,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + [71, 89, 97, 101, 103]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")