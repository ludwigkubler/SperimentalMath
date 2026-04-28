# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def generate_random_3cnf(n, m, alpha):
    clauses = set()
    while len(clauses) < m:
        clause = []
        for _ in range(3):
            var = random.randint(1, n)
            sign = random.choice([-1, 1])
            if (var, sign) not in clause and (-var, -sign) not in clause:
                clause.append((var, sign))
        if len(clause) == 3:
            clauses.add(tuple(sorted(clause)))
    return clauses

def lex_dpll(F, budget):
    n = max(abs(var) for var, _ in F)
    assignment = [0] * (n + 1)
    stack = []
    leaves = 0
    while stack or len(stack) < budget:
        if not stack:
            stack.append((set(), 0))
        path, i = stack.pop()
        if i == n + 1:
            leaves += 1
            continue
        for sign in [-1, 1]:
            new_path = path | {(i, sign)}
            if all(any(clause[j] != (var, sign) for clause in F) for j in range(n)):
                stack.append((new_path, i + 1))
    return leaves

def signed_incidence_matrix(F):
    n = max(abs(var) for var, _ in F)
    m = len(F)
    A = [[0] * n for _ in range(m)]
    for i, clause in enumerate(F):
        for var, sign in clause:
            A[i][var - 1] = sign
    return A

def determinant(A):
    if not A or not A[0]:
        return 0
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1) ** j * A[0][j] * determinant(submatrix)
    return det

def max_row_norm(A):
    n, m = len(A), len(A[0])
    norms = [sum(abs(A[i][j]) for j in range(m)) for i in range(n)]
    return max(norms)

def greedy_max_norm_selection(A, k):
    rows = list(range(len(A)))
    selected_rows = []
    while len(selected_rows) < k:
        norm = max_row_norm([A[i] for i in rows])
        selected_rows.append(rows.pop(rows.index(max_row_norm([A[i] for i in rows]))))
    return [A[i] for i in selected_rows]

def detlb(F):
    A = signed_incidence_matrix(F)
    n, m = len(A), len(A[0])
    k_max = min(8, m, n)
    samples = 5000
    if math.comb(m, k_max) <= samples:
        rows = list(range(m))
    else:
        rows = random.sample(list(range(m)), samples)
    max_det = float('-inf')
    for row_subset in combinations(rows, k_max):
        M_S = [A[i] for i in row_subset]
        det = determinant(M_S)
        if abs(det) > max_det:
            max_det = abs(det)
    return max_det ** (1 / k_max)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [8, 10, 12, 14, 16, 18, 20]
    alpha_values = [4.0, 4.5, 5.0]
    c_emp_min = float('inf')
    counterexample = ""
    
    for n in n_values:
        for alpha in alpha_values:
            m = int(n * alpha)
            F = generate_random_3cnf(n, m, alpha)
            leaves = lex_dpll(F, 30e6)
            detlb_val = detlb(F)
            if detlb_val == 0:
                counterexample = "detlb_zero"
                break
            c_emp = math.log2(leaves + 1) / (detlb_val * math.sqrt(n))
            if c_emp < c_emp_min:
                c_emp_min = c_emp
    
    return {
        "metric_name": "c_emp",
        "metric_value": c_emp_min,
        "instances_tested": len(n_values) * len(alpha_values),
        "conjecture_holds": c_emp_min >= 0.20,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    c_emp_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = len(c_emp_values) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(c_emp_values)/len(c_emp_values):.4f} std={math.sqrt(sum((x - sum(c_emp_values)/len(c_emp_values))**2 for x in c_emp_values) / len(c_emp_values)):.4f} support_fraction={support_fraction:.4f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")