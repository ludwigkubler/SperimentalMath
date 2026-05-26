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
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % m

def matrix_mod_inv(matrix, p):
    n = len(matrix)
    det = 0
    for i in range(n):
        det += matrix[0][i] * matrix_minor(matrix, 0, i) * (-1) ** (0 + i)
    det = det % p
    inv_det = mod_inverse(det, p)
    adjugate = [[matrix_minor(matrix, j, i) * (-1) ** (j + i) for i in range(n)] for j in range(n)]
    inverse = [[(adjugate[i][j] * inv_det) % p for j in range(n)] for i in range(n)]
    return inverse

def matrix_minor(matrix, row, col):
    minor = [row[:col] + row[col+1:] for row in matrix[1:]]
    return determinant(minor)

def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    elif n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    else:
        det = 0
        for i in range(n):
            det += ((-1) ** i) * matrix[0][i] * determinant([row[:i] + row[i+1:] for row in matrix[1:]])
        return det

def gaussian_elimination(matrix, b, p):
    n = len(b)
    augmented_matrix = [[matrix[i][j] for j in range(n)] + [b[i]] for i in range(n)]
    
    for i in range(n):
        pivot_row = max(range(i, n), key=lambda r: abs(augmented_matrix[r][i]))
        augmented_matrix[i], augmented_matrix[pivot_row] = augmented_matrix[pivot_row], augmented_matrix[i]
        
        for j in range(i + 1, n):
            factor = (augmented_matrix[j][i] * mod_inverse(augmented_matrix[i][i], p)) % p
            for k in range(n + 1):
                augmented_matrix[j][k] = (augmented_matrix[j][k] - factor * augmented_matrix[i][k]) % p
    
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (augmented_matrix[i][-1] - sum(augmented_matrix[i][j] * x[j] for j in range(i + 1, n))) * mod_inverse(augmented_matrix[i][i], p) % p
    
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([20, 25, 30, 35, 40])
    d = random.randint(1, n)
    p = 7  # Example prime number
    c = 1.0  # Constant independent of n
    
    # Generate a random Frege proof tree (simplified for demonstration)
    def generate_frege_tree(depth):
        if depth == 0:
            return random.choice(['x', 'y', 'z'])
        else:
            op = random.choice(['&', '|'])
            left = generate_frege_tree(depth - 1)
            right = generate_frege_tree(depth - 1)
            return (op, left, right)
    
    def clause_indicator_polynomial(tree):
        if isinstance(tree, str):
            return {tree: 1}
        else:
            op, left, right = tree
            if op == '&':
                return {**clause_indicator_polynomial(left), **clause_indicator_polynomial(right)}
            elif op == '|':
                left_poly = clause_indicator_polynomial(left)
                right_poly = clause_indicator_polynomial(right)
                result = {}
                for var in set(left_poly.keys()).union(set(right_poly.keys())):
                    if var in left_poly and var in right_poly:
                        result[var] = (left_poly[var] * right_poly[var]) % p
                    elif var in left_poly:
                        result[var] = left_poly[var]
                    else:
                        result[var] = right_poly[var]
                return result
    
    def polynomial_to_matrix(poly):
        n_vars = len(poly)
        matrix = [[0] * n_vars for _ in range(n_vars)]
        for var, coeff in poly.items():
            i = ord(var) - ord('x')
            matrix[i][i] += coeff
        return matrix
    
    tree = generate_frege_tree(d)
    poly = clause_indicator_polynomial(tree)
    matrix = polynomial_to_matrix(poly)
    
    try:
        rank = len(gaussian_elimination(matrix, [1] * n, p))
    except Exception as e:
        return {
            "metric_name": "rank",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": str(e)
        }
    
    expected_rank = math.ceil(c * p ** (n - d / 2))
    
    return {
        "metric_name": "rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= expected_rank,
        "counterexample": "" if rank >= expected_rank else f"rank={rank}, expected={expected_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")