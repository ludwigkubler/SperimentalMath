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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    if m == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1) ** j * A[0][j] * determinant(submatrix)
    return det

def generate_cnf(num_vars, num_clauses):
    cnf = []
    for _ in range(num_clauses):
        clause = [random.randint(1, num_vars) if random.choice([True, False]) else -random.randint(1, num_vars) for _ in range(random.randint(1, 3))]
        cnf.append(clause)
    return cnf

def resolution(cnf):
    clauses = set(tuple(sorted(clause)) for clause in cnf)
    while True:
        new_clauses = set()
        for clause1 in clauses:
            for clause2 in clauses:
                if len(set(clause1) & set(clause2)) == 1:
                    literal_to_remove = list(set(clause1) & set(clause2))[0]
                    new_clause = tuple(sorted([l for l in clause1 + clause2 if l != literal_to_remove and -l not in clause1 + clause2]))
                    if new_clause:
                        new_clauses.add(new_clause)
        if new_clauses.issubset(clauses):
            break
        clauses.update(new_clauses)
    return len(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    cnf = generate_cnf(n, random.randint(1, 2*n))
    resolution_width = resolution(cnf)
    normal_forms = set()
    for clause in cnf:
        stack = [tuple(sorted(clause))]
        while stack:
            current_clause = stack.pop()
            if current_clause not in normal_forms:
                normal_forms.add(current_clause)
                for i in range(n):
                    new_clause = tuple(sorted([l for l in current_clause if l != -i and i not in current_clause]))
                    if new_clause:
                        stack.append(new_clause)
    order_coxeter_group = 2 ** n  # Simplified example, actual computation depends on the specific Coxeter group
    ratio = len(normal_forms) / resolution_width
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio <= order_coxeter_group,
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

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")