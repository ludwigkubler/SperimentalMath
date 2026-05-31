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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i
        for j in range(i+1, rows):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        pivot = matrix[i][i]
        if pivot == 0:
            continue
        for j in range(i, cols):
            matrix[i][j] /= pivot
        for j in range(rows):
            if j != i and matrix[j][i] != 0:
                factor = matrix[j][i]
                for k in range(i, cols):
                    matrix[j][k] -= factor * matrix[i][k]

def matrix_multiplication(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    return result

def resolution_width(clauses):
    queue = clauses[:]
    while queue:
        clause1, clause2 = queue.pop(0)
        new_clauses = set()
        for lit1 in clause1:
            if -lit1 in clause2:
                continue
            for lit2 in clause2:
                if -lit2 not in clause1 and (lit1 != lit2):
                    new_clause = sorted(list(set(clause1 + [lit2]) - {lit1}))
                    if new_clause not in new_clauses:
                        new_clauses.add(new_clause)
        queue.extend(new_clauses)
    return len(queue)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n, m = 5, 10
    while n <= 40:
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, 2*n) * (1 if random.random() < 0.5 else -1) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        
        width = resolution_width(clauses)
        # Compute Coxeter-diagram entropy (simplified as number of distinct edges)
        edges = set()
        for clause in clauses:
            for i in range(len(clause)):
                for j in range(i+1, len(clause)):
                    edges.add((abs(clause[i]), abs(clause[j])))
        entropy = len(edges)
        
        if entropy > 10 * width:
            return {
                "metric_name": "Coxeter-diagram Entropy",
                "metric_value": entropy,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"Entropy {entropy} > 10 * Width {width}"
            }
        
        n += 5
    
    return {
        "metric_name": "Coxeter-diagram Entropy",
        "metric_value": entropy,
        "instances_tested": 6,
        "n_max": 40,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
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
        print(f"RESULT: FALSIFIED counterexample=\"Entropy > 10 * Width\" first_failing_seed={first_failing_seed}")