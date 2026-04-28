# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def gaussian_elimination(A):
    n = len(A)
    m = len(A[0])
    rank = 0
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            continue
        rank += 1
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(m):
                A[j][k] -= factor * A[i][k]
    return rank

def matrix_multiply(A, B):
    n = len(A)
    m = len(B[0])
    p = len(B)
    C = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    sign = 1
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += sign * A[0][j] * determinant(submatrix)
        sign *= -1
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3cnf(n, alpha):
        m = int(alpha * n * (n - 1) // 2)
        clauses = set()
        while len(clauses) < m:
            a, b, c = random.sample(range(n), 3)
            clause = tuple(sorted([a, b, c]))
            if clause not in clauses:
                clauses.add(clause)
        return clauses
    
    def lex_dpll(F):
        n = len(F)
        unit_propagation = [False] * n
        for _ in range(2 ** n):
            assignment = [i % 2 == 1 for i in range(n)]
            if all(any(lit in clause for lit in assignment) or any(-lit in clause for lit in assignment) for clause in F):
                return True, assignment
        return False, None
    
    def build_Q_F(F, n):
        monomials = defaultdict(int)
        for a, b, c in F:
            monomial = (a, b, c)
            monomials[monomial] += 1
        return monomials
    
    def build_M_11(Q_F, n):
        m_11 = []
        for i in range(n + 1):
            row = [0] * ((n + 3) * (n + 2) // 6)
            for a, b, c in Q_F:
                if a == i or b == i or c == i:
                    index = (a + b + c - 3) * (a + b + c - 4) // 2 + a + b + c - 1
                    row[index] += Q_F[(a, b, c)]
            m_11.append(row)
        return m_11
    
    def build_Cat_1(Q_F, n):
        cat_1 = []
        for i in range(n + 1):
            row = [0] * ((n + 2) * (n + 1) // 2)
            for a, b, c in Q_F:
                if a == i or b == i or c == i:
                    index = (a + b - 2) * (a + b - 1) // 2 + a
                    row[index] += Q_F[(a, b, c)]
            cat_1.append(row)
        return cat_1
    
    def log2_floor(x):
        if x <= 0:
            return -math.inf
        return math.floor(math.log2(x))
    
    n = random.choice([8, 10, 12, 14, 16])
    alpha = random.uniform(4.5, 5.5)
    F = generate_3cnf(n, alpha)
    unsat, _ = lex_dpll(F)
    if not unsat:
        return {
            "metric_name": "ψ(F)",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "unsat_instance"
        }
    
    Q_F = build_Q_F(F, n)
    M_11 = build_M_11(Q_F, n)
    Cat_1 = build_Cat_1(Q_F, n)
    
    rank_M_11 = gaussian_elimination(M_11)
    rank_Cat_1 = gaussian_elimination(Cat_1)
    
    psi_F = rank_M_11 - rank_Cat_1
    L_T = 2 ** (len(F) / n)
    log2_L_T = log2_floor(L_T)
    
    return {
        "metric_name": "ψ(F)",
        "metric_value": psi_F,
        "instances_tested": 1,
        "conjecture_holds": psi_F >= log2_L_T,
        "counterexample": "" if psi_F >= log2_L_T else f"psi_F={psi_F}, log2(L_T)={log2_L_T}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(res["metric_value"] for res in results if res["metric_value"] is not None)
    num_trials = len(results)
    mean_metric_value = total_metric_value / num_trials
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results if res["metric_value"] is not None) / (num_trials - 1))
    
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / num_trials
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] and res["metric_value"] < math.floor(math.log2(2 ** (len(F) / n))) - 1 for res in results):
        print(f"RESULT: FALSIFIED counterexample=\"psi_F<floor(log2(L_T))−1\" first_failing_seed={seeds[next(i for i, res in enumerate(results) if not res['conjecture_holds'] and res['metric_value'] < math.floor(math.log2(2 ** (len(F) / n))) - 1)]})")
    else:
        print(f"RESULT: INCONCLUSIVE insufficient_data")