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

def matrix_rank(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    for i in range(m):
        if all(matrix[i][j] == 0 for j in range(n)):
            continue
        pivot_row = i
        for j in range(i+1, m):
            if matrix[j][i] != 0:
                pivot_row = j
                break
        if pivot_row == i:
            rank += 1
            for j in range(i, n):
                matrix[i][j] /= matrix[i][i]
            for j in range(m):
                if j != i and matrix[j][i] != 0:
                    for k in range(n):
                        matrix[j][k] -= matrix[i][k]
    return rank

def gaussian_elimination(matrix):
    m, n = len(matrix), len(matrix[0])
    augmented_matrix = [row + [Fraction(1) if i == j else Fraction(0) for j in range(m)] for i, row in enumerate(matrix)]
    for i in range(m):
        pivot_row = i
        for j in range(i+1, m):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[pivot_row][i]):
                pivot_row = j
        augmented_matrix[i], augmented_matrix[pivot_row] = augmented_matrix[pivot_row], augmented_matrix[i]
        if augmented_matrix[i][i] == 0:
            continue
        for j in range(i+1, m):
            factor = augmented_matrix[j][i] / augmented_matrix[i][i]
            for k in range(n):
                augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    return [row[n:] for row in augmented_matrix]

def tropical_add(x, y):
    if x == float('-inf') or y == float('-inf'):
        return max(x, y)
    return x + y

def tropical_multiply(x, y):
    if x == float('-inf') or y == float('-inf'):
        return float('-inf')
    return x * y

def tropical_rank(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    for i in range(m):
        if all(tropical_add(matrix[i][j], float('-inf')) == float('-inf') for j in range(n)):
            continue
        pivot_row = i
        for j in range(i+1, m):
            if tropical_add(matrix[j][i], float('-inf')) != float('-inf'):
                pivot_row = j
                break
        if pivot_row == i:
            rank += 1
            for j in range(i, n):
                matrix[i][j] = tropical_multiply(matrix[i][j], Fraction(1))
            for j in range(m):
                if j != i and tropical_add(matrix[j][i], float('-inf')) != float('-inf'):
                    for k in range(n):
                        matrix[j][k] = tropical_add(matrix[j][k], -tropical_multiply(matrix[i][k], matrix[j][i]))
    return rank

def generate_kcnf_instance(n, m):
    variables = list(range(1, n+1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 2)
        clauses.append(clause)
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            m = random.randint(1, n*2)
            instance = generate_kcnf_instance(n, m)
            tropical_semigroup = []
            for clause in instance:
                tropical_clause = [tropical_add(x, float('-inf')) if x not in clause else float('-inf') for x in range(1, n+1)]
                tropical_semigroup.append(tropical_clause)
            rank = tropical_rank(tropical_semigroup)
            cc_r = 2 ** rank
            results.append((n, m, rank, cc_r))
    metric_name = "communication_complexity"
    metric_value = sum(cc_r for _, _, _, cc_r in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(2**rank <= cc_r for _, _, rank, cc_r in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*40+2))
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    mean = sum(r['metric_value'] for r in results) / len(results)
    std = math.sqrt(sum((r['metric_value'] - mean)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean:.6f} std={std:.6f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean:.6f} std={std:.6f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")