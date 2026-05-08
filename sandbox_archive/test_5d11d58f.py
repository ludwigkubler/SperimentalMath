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
    det = 0
    for i in range(n):
        det += matrix[0][i] * matrix_minor(matrix, 0, i) * (-1) ** (0 + i)
    det = det % mod
    inv_det = mod_inverse(det, mod)
    adjugate = [[matrix_minor(matrix, j, i) * (-1) ** (j + i) for i in range(n)] for j in range(n)]
    inverse = [[(adjugate[i][j] * inv_det) % mod for j in range(n)] for i in range(n)]
    return inverse

def matrix_minor(matrix, row, col):
    minor = [row[:col] + row[col+1:] for row in matrix[1:]]
    return determinant(minor)

def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    for i in range(n):
        det += ((-1) ** i) * matrix[0][i] * determinant([row[:i] + row[i+1:] for row in matrix[1:]])
    return det

def gaussian_elimination(matrix, b):
    n = len(matrix)
    augmented_matrix = [row + [b[i]] for i, row in enumerate(matrix)]
    for i in range(n):
        max_row = max(range(i, n), key=lambda k: abs(augmented_matrix[k][i]))
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        factor = augmented_matrix[i][i]
        for j in range(i, n + 1):
            augmented_matrix[i][j] /= factor
        for k in range(n):
            if k != i:
                factor = augmented_matrix[k][i]
                for j in range(i, n + 1):
                    augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
    return [row[-1] for row in augmented_matrix]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    N = random.choice([4, 6, 9])
    d = random.choice([3, 4]) if N == 4 else random.choice([3])
    s_values = [3, 5, 8, 12, 16, 24, 32]
    results = []
    
    for s in s_values:
        formulas = generate_formulas(N, d, s)
        for f in formulas:
            rLS = compute_rLS(f, N, d)
            results.append({"s": s, "rLS": rLS})
    
    max_diff = max(result["rLS"] - 4 * result["s"] for result in results)
    conjecture_holds = max_diff <= 0
    counterexample = "" if conjecture_holds else f"max(rLS-4s)={max_diff}"
    
    return {
        "metric_name": "rLS",
        "metric_value": max_diff,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def generate_formulas(N, d, s):
    leaves = list(range(1, N + 1)) + [random.randint(-5, 5) for _ in range(s - N)]
    formulas = set()
    
    def build_tree(depth, path):
        if depth == s:
            formula = evaluate_formula(path)
            if all(f != 0 for f in formula):
                formulas.add(tuple(sorted(formula.items())))
            return
        for leaf in leaves:
            new_path = path + [leaf]
            build_tree(depth + 1, new_path)
    
    def evaluate_formula(path):
        stack = []
        for token in path:
            if isinstance(token, int):
                stack.append(token)
            else:
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
        return stack[0]
    
    build_tree(0, [])
    return formulas

def compute_rLS(f, N, d):
    monomials = list(f.keys())
    n = len(monomials)
    matrix = [[0] * (N ** 2) for _ in range(n)]
    
    def get_coefficient(monomial):
        coeff = 1
        for var, exp in monomial.items():
            coeff *= math.comb(N, var - 1) * (var - 1) ** (exp - 1)
        return coeff
    
    for i, m1 in enumerate(monomials):
        for j, m2 in enumerate(monomials):
            for k in range(1, N + 1):
                if k not in m1 and k not in m2:
                    continue
                diff = sum((m1.get(k, 0) - m2.get(k, 0)) * get_coefficient({k: exp}) for k, exp in m1.items() if k != k)
                matrix[i][j] += diff
    
    rank = gaussian_elimination(matrix, [0] * n).count(0)
    return N ** 2 - 1 - rank

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    max_diff = max(result["rLS"] - 4 * result["s"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if max_diff <= 0 and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(result['metric_value'] for result in results) / len(results)} std=0 support_fraction={support_fraction}")
    elif any(result["rLS"] > 4 * result["s"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["rLS"] > 4 * result["s"])
        print(f"RESULT: FALSIFIED counterexample=\"max(rLS-4s)>0\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")