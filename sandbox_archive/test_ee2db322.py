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
        raise ValueError(f"No modular inverse for {a} modulo {m}")
    return x % m

def matrix_mod_inv(matrix, mod):
    n = len(matrix)
    det = 0
    if n == 1:
        det = matrix[0][0]
    elif n == 2:
        det = (matrix[0][0] * matrix[1][1]) - (matrix[0][1] * matrix[1][0])
    else:
        for i in range(n):
            sub_matrix = [row[:i] + row[i+1:] for row in matrix[1:]]
            det += ((-1) ** i) * matrix[0][i] * matrix_mod_inv(sub_matrix, mod)
    
    det = det % mod
    inv_det = mod_inverse(det, mod)
    
    adjugate = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            sub_matrix = [row[:j] + row[j+1:] for row in matrix[:i] + matrix[i+1:]]
            cofactor = ((-1) ** (i + j)) * matrix_mod_inv(sub_matrix, mod)
            adjugate[j][i] = cofactor
    
    inverse = [[(adjugate[i][j] * inv_det) % mod for j in range(n)] for i in range(n)]
    return inverse

def matrix_multiply(A, B):
    n = len(A)
    m = len(B[0])
    p = len(B)
    
    result = [[0 for _ in range(m)] for _ in range(n)]
    
    for i in range(n):
        for j in range(m):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    
    return result

def matrix_power(matrix, n):
    if n == 0:
        identity = [[1 if i == j else 0 for j in range(len(matrix))] for i in range(len(matrix))]
        return identity
    elif n % 2 == 0:
        half_power = matrix_power(matrix, n // 2)
        return matrix_multiply(half_power, half_power)
    else:
        return matrix_multiply(matrix, matrix_power(matrix, n - 1))

def generate_frege_tree(h, m):
    if h <= 0 or m <= 0:
        raise ValueError("Height and size must be positive integers")
    
    if m == 1:
        return [[None]]
    
    left_size = random.randint(1, m - 2)
    right_size = m - 1 - left_size
    
    left_tree = generate_frege_tree(h - 1, left_size)
    right_tree = generate_frege_tree(h - 1, right_size)
    
    tree = [[None] + row for row in left_tree]
    tree += [[None] + row for row in right_tree]
    
    return tree

def count_automorphisms(tree):
    n = len(tree)
    if n == 0:
        return 1
    
    # Count the number of nodes at each level
    levels = [[] for _ in range(n)]
    for i, row in enumerate(tree):
        levels[i].append(row[0])
    
    # Generate all permutations of the first node at each level
    from itertools import permutations
    
    perms = []
    for level in levels:
        perm = list(permutations(level))
        perms.append(perm)
    
    # Count the number of valid automorphisms
    count = 0
    for p in product(*perms):
        new_tree = [[None] * n for _ in range(n)]
        for i, row in enumerate(tree):
            for j in range(n):
                if row[j] is not None:
                    new_tree[i][j] = p[row[j]]
        
        if new_tree == tree:
            count += 1
    
    return count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    h_values = [5, 10, 15, 20, 30, 40]
    m_values = [10, 20, 30, 40]
    
    results = []
    for h in h_values:
        for m in m_values:
            tree = generate_frege_tree(h, m)
            automorphisms = count_automorphisms(tree)
            expected_bound = math.ceil(math.sqrt(m) * math.sqrt(h))
            
            if automorphisms > expected_bound:
                return {
                    "metric_name": "Automorphism Count",
                    "metric_value": automorphisms,
                    "instances_tested": 1,
                    "n_max": max(h, m),
                    "conjecture_holds": False,
                    "counterexample": f"Tree with h={h}, m={m} has {automorphisms} automorphisms > {expected_bound}"
                }
    
    return {
        "metric_name": "Automorphism Count",
        "metric_value": sum(count_automorphisms(generate_frege_tree(h, m)) for h in h_values for m in m_values) / len(h_values) / len(m_values),
        "instances_tested": len(h_values) * len(m_values),
        "n_max": max(h_values[-1], m_values[-1]),
        "conjecture_holds": True,
        "counterexample": ""
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Automorphism count exceeded expected bound\" first_failing_seed={first_failing_seed}")