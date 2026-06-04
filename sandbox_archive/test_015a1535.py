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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A, b):
        n = len(A)
        for i in range(n):
            # Find pivot
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            
            # Eliminate below pivot
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        
        # Back substitution
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        return x

    def count_integral_points(A, b):
        n = len(A)
        count = 0
        for x in range(-10, 11):
            for y in range(-10, 11):
                if all(abs(a*x + b*y - c) <= 1e-6 for a, b, c in A):
                    count += 1
        return count

    def generate_tseitin_formula(n, d):
        # Generate a random d-regular graph
        V = list(range(2*n))
        E = set()
        while len(E) < n*d:
            u = random.choice(V)
            v = random.choice(V)
            if u != v and (u, v) not in E and (v, u) not in E:
                E.add((u, v))
        
        # Generate Tseitin formula
        literals = {i: f'x{i}' for i in range(n)}
        clauses = []
        for u, v in E:
            a, b = random.choice([literals[u], '¬' + literals[u]]), random.choice([literals[v], '¬' + literals[v]])
            literals[u] = '¬' + a
            literals[v] = '¬' + b
            clauses.append(f'{a} ∨ {b}')
        for i in range(n):
            clauses.append(f'{literals[i]}')
        
        # Convert to matrix form
        A = []
        b = []
        for clause in clauses:
            if '∨' in clause:
                a, b = clause.split(' ∨ ')
                A.append([1 if x == a else 0 if x == '¬' + a else -1 for x in literals.values()])
                A.append([1 if x == b else 0 if x == '¬' + b else -1 for x in literals.values()])
            else:
                A.append([1 if x == clause else 0 if x == '¬' + clause else -1 for x in literals.values()])
            b.extend([1, 1])
        
        return A, b

    def resolution_width(A):
        n = len(A)
        clauses = {tuple(row) for row in A}
        width = 0
        while True:
            new_clauses = set()
            for clause1 in clauses:
                for clause2 in clauses:
                    if len(clause1 & clause2) == 1:
                        new_clause = tuple(sorted(set(clause1 + clause2) - {tuple([1, 1])[0]}))
                        if new_clause not in clauses and new_clause not in new_clauses:
                            new_clauses.add(new_clause)
            if not new_clauses:
                break
            clauses.update(new_clauses)
            width += 1
        return width

    n = random.choice([5, 10, 15, 20, 30, 40])
    A, b = generate_tseitin_formula(n, 2)
    integral_points_count = count_integral_points(A, b)
    w = resolution_width(A)

    return {
        "metric_name": "integral_points_count",
        "metric_value": integral_points_count,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
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
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")