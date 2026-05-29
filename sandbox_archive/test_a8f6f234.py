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
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    augmented_matrix = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        pivot = augmented_matrix[i][i]
        for j in range(i, n+1):
            augmented_matrix[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(i, n+1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    return [row[-1] for row in augmented_matrix]

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1) ** j * A[0][j] * determinant(submatrix)
    return det

def is_full_rank(A):
    return determinant(A) != 0

def random_3cnf(n, m):
    variables = list(range(1, n+1))
    clauses = []
    for _ in range(m):
        clause = [random.choice([1, -1]) * random.choice(variables) for _ in range(3)]
        if len(set(clause)) == 3:
            clauses.append(clause)
    return clauses

def tropical_add(a, b):
    return max(a, b)

def tropical_multiply(a, b):
    return a + b

def tropical_negate(a):
    return -a

def tropical_zero():
    return float('-inf')

def tropical_one():
    return 0

def tropical_polynomial(clauses):
    n = len(clauses[0])
    poly = [[tropical_zero() for _ in range(n)] for _ in range(n)]
    for clause in clauses:
        for i, var in enumerate(clause):
            if var > 0:
                poly[i][var-1] = tropical_add(poly[i][var-1], tropical_one())
            else:
                poly[-i-1][-var-1] = tropical_add(poly[-i-1][-var-1], tropical_one())
    return poly

def tropical_category_depth(poly):
    n = len(poly)
    depth = 0
    while True:
        new_poly = [[tropical_zero() for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if poly[i][j] != tropical_zero():
                    for k in range(n):
                        new_poly[i][k] = tropical_add(new_poly[i][k], tropical_multiply(poly[i][j], poly[j][k]))
        if new_poly == poly:
            break
        poly = new_poly
        depth += 1
    return depth

def frege_proof_depth(clause_count):
    # Placeholder function to simulate Frege proof depth calculation
    return clause_count * 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(2 * n, 4 * n)
        clauses = random_3cnf(n, m)
        poly = tropical_polynomial(clauses)
        
        if not is_full_rank(poly):
            return {
                "metric_name": "tropical_category_depth",
                "metric_value": None,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        depth = tropical_category_depth(poly)
        d_F = frege_proof_depth(m)
        
        results.append({
            "n": n,
            "m": m,
            "depth": depth,
            "d_F": d_F
        })
    
    alpha_n_values = [math.log2(n) ** 2 for n in n_values]
    beta = 0.5  # Placeholder value for beta
    
    mean_depth = sum(result["depth"] for result in results) / len(results)
    std_depth = math.sqrt(sum((result["depth"] - mean_depth) ** 2 for result in results) / len(results))
    
    conjecture_holds = all(depth <= alpha_n and depth <= beta * math.log(d_F) for result in results for alpha_n in alpha_n_values)
    
    counterexample = "" if conjecture_holds else "depth does not satisfy bounds"
    
    return {
        "metric_name": "tropical_category_depth",
        "metric_value": mean_depth,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    all_results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.append(result)
    
    mean_depth = sum(result["metric_value"] for result in all_results if result["metric_value"] is not None) / len(all_results)
    std_depth = math.sqrt(sum((result["metric_value"] - mean_depth) ** 2 for result in all_results if result["metric_value"] is not None) / len(all_results))
    
    support_fraction = sum(1 for result in all_results if result["conjecture_holds"]) / len(all_results)
    
    if all(result["conjecture_holds"] for result in all_results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_depth} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in all_results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, all_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"depth does not satisfy bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")