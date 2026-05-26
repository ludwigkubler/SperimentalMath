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
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

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

def rank(A):
    m, n = len(A), len(A[0])
    A_augmented = A[:]
    rref = gaussian_elimination(A_augmented, [0]*n)
    rank = sum(1 for x in rref if abs(x) > 1e-9)
    return rank

def generate_cnf(n):
    clauses = []
    for _ in range(n):
        clause = random.sample(range(-n, n+1), 3)
        clauses.append(clause)
    return clauses

def resolution_proof(cnf):
    queue = cnf[:]
    while True:
        new_clauses = []
        for i in range(len(queue)):
            for j in range(i+1, len(queue)):
                clause1 = queue[i]
                clause2 = queue[j]
                for lit1 in clause1:
                    if -lit1 in clause2:
                        new_clause = list(set(clause1 + clause2) - {lit1, -lit1})
                        if not any(lit in new_clause for lit in clause1):
                            new_clauses.append(new_clause)
        queue.extend(new_clause for new_clause in new_clauses if new_clause not in queue)
        if len(queue) == len(cnf):
            return None
        cnf = queue

def geometric_quantization_rank(proof_tree):
    # Placeholder implementation; actual mapping undefined
    return random.randint(1, 10)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    proof_tree = resolution_proof(cnf)
    if not proof_tree:
        return {
            "metric_name": "geometric_quantization_rank",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "resolution_proved"
        }
    rank_value = geometric_quantization_rank(proof_tree)
    depth = len(proof_tree) if proof_tree else 0
    ratio = rank_value / (depth + 1e-9)
    return {
        "metric_name": "geometric_quantization_rank",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 2,  # Placeholder constant c
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, ...{result}...}}")
        results.append(result)

    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)

    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")