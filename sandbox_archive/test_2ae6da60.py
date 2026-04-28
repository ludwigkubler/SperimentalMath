# auto-injected by SEC sandbox
import itertools
import collections
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
import json

def generate_3cnf(n, m, alpha):
    clauses = set()
    while len(clauses) < m:
        clause = []
        for _ in range(3):
            var = random.randint(-n, n)
            if var not in clause and -var not in clause:
                clause.append(var)
        if len(clause) == 3:
            clauses.add(tuple(sorted(clause)))
    return list(clauses)

def lex_dpll(F, budget):
    n = max(abs(var) for var, _ in F)
    assignment = [None] * (n + 1)
    stack = []
    leaves = 0
    def dpll():
        nonlocal leaves
        if len(stack) == n:
            leaves += 1
            return True
        var = next((i for i in range(1, n + 1) if assignment[i] is None), None)
        if var is None:
            return False
        assignment[var] = True
        stack.append(var)
        if all(any(clause[i - 1] != assignment[abs(clause[i - 1])] for i in clause) for clause in F):
            if dpll():
                return True
        assignment[var] = False
        stack.pop()
        assignment[-var] = True
        stack.append(-var)
        if all(any(clause[i - 1] != assignment[abs(clause[i - 1])] for i in clause) for clause in F):
            if dpll():
                return True
        assignment[-var] = None
        stack.pop()
        return False
    dpll()
    return leaves

def signed_incidence_matrix(F, n):
    m = len(F)
    M = [[0] * n for _ in range(m)]
    for i, clause in enumerate(F):
        for var in clause:
            M[i][abs(var) - 1] = 1 if var > 0 else -1
    return M

def max_row_norm(M):
    return max(sum(abs(x) for x in row) for row in M)

def submatrix_determinant(M, S):
    m = len(S)
    n = len(S[0])
    M_S = [[M[i][j] for j in S[0]] for i in range(m)]
    det = 1
    for i in range(n):
        max_row = -1
        max_norm = -1
        for r in range(i, m):
            norm = sum(abs(M_S[r][c]) for c in range(n))
            if norm > max_norm:
                max_row = r
                max_norm = norm
        M_S[i], M_S[max_row] = M_S[max_row], M_S[i]
        det *= M_S[i][i]
        if det == 0:
            return 0
        for r in range(i + 1, m):
            factor = M_S[r][i] / M_S[i][i]
            for c in range(n):
                M_S[r][c] -= factor * M_S[i][c]
    return det

def detlb(F, n):
    m = len(F)
    k_max = min(8, m, n)
    samples = 5000 if math.comb(m, k_max) > 5000 else math.comb(m, k_max)
    max_det = -1
    for _ in range(samples):
        S = random.sample(range(n), k_max)
        det = submatrix_determinant(F, [S])
        if det > max_det:
            max_det = det
    return max_det ** (1 / k_max)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [8, 10, 12, 14, 16, 18, 20]
    alpha_values = [4.0, 4.5, 5.0]
    c_emp = float('inf')
    counterexample = ""
    for n in n_values:
        for alpha in alpha_values:
            F = generate_3cnf(n, int(alpha * n * (n - 1) / 6), alpha)
            leaves = lex_dpll(F, 30e6)
            if leaves == 0:
                continue
            detlb_val = detlb(F, n)
            c = math.log2(leaves + 1) / (detlb_val * math.sqrt(n))
            if c < c_emp:
                c_emp = c
                counterexample = f"n={n}, alpha={alpha}"
    return {
        "metric_name": "c_emp",
        "metric_value": c_emp,
        "instances_tested": len(n_values) * len(alpha_values),
        "conjecture_holds": c_emp >= 0.20,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    mean_c_emp = sum(r["metric_value"] for r in results) / len(results)
    std_c_emp = math.sqrt(sum((r["metric_value"] - mean_c_emp) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_c_emp} std={std_c_emp} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")