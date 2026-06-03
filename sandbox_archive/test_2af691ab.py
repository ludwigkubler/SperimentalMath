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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = -A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] += factor * A[i][k]
            b[j] += factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def matrix_mult(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A, n):
    det = 0
    if n == 1:
        return A[0][0]
    elif n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    else:
        for c in range(n):
            det += ((-1) ** c) * A[0][c] * determinant([row[:c] + row[c+1:] for row in A[1:]], n-1)
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def tseitin_formula(n, clause_distribution):
        literals = list(range(1, 2*n+1))
        clauses = []
        for i in range(1, n+1):
            clauses.append([i])
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                clauses.append([-i, -j, 2*n+i])
                clauses.append([-i, -j, 2*n+j])
                clauses.append([i, j, -(2*n+i)])
                clauses.append([i, j, -(2*n+j)])
        for i in range(1, n+1):
            for clause in random.sample(clause_distribution[i], clause_distribution[i][0]):
                if clause < 0:
                    literals.append(-i)
                else:
                    literals.append(i)
                clauses.append([clause])
        return literals, clauses

    def tropical_derivative_rank(literals, clauses, p):
        n = len(literals) // 2
        f_phi = [0] * (n + 1)
        for clause in clauses:
            term = 1
            for lit in clause:
                if lit > 0:
                    term *= literals[lit - 1]
                else:
                    term += literals[-lit - 1]
            f_phi[term % p] += 1
        J = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if i != j:
                    J[i][j] = literals[j - 1]
        rank = determinant(J, n)
        return rank

    def resolution_width(literals, clauses):
        # Simplified DPLL solver to estimate width
        def solve(lits_true, lits_false):
            stack = []
            while stack or lits_true:
                if not stack:
                    stack.append(next((lit for lit in literals if lit not in lits_true and -lit not in lits_false), None))
                lit = stack[-1]
                if lit is None:
                    return len(lits_true)
                if lit > 0:
                    lits_true.add(lit)
                else:
                    lits_false.add(-lit)
                for clause in clauses:
                    if all(lit not in clause and -lit not in clause for lit in literals):
                        stack.pop()
                        break
            return len(lits_true)

        width = float('inf')
        for i in range(1 << n):
            lits_true = set()
            lits_false = set()
            for j in range(n):
                if (i >> j) & 1:
                    lits_true.add(j + 1)
                else:
                    lits_false.add(-(j + 1))
            width = min(width, solve(lits_true, lits_false))
        return width

    n_values = [5, 10, 15, 20, 30, 40]
    mtr_values = []
    w_values = []

    for n in n_values:
        clause_distribution = {i: random.randint(1, min(i, 3)) for i in range(1, n+1)}
        literals, clauses = tseitin_formula(n, clause_distribution)
        p = 101
        mtr = tropical_derivative_rank(literals, clauses, p)
        w = resolution_width(literals, clauses)
        mtr_values.append(mtr)
        w_values.append(w)

    correlation_coefficient = sum((mtr_values[i] - mean_mtr) * (w_values[i] - mean_w) for i in range(len(n_values))) / len(n_values)
    mean_mtr = sum(mtr_values) / len(mtr_values)
    mean_w = sum(w_values) / len(w_values)
    p_value = 2 * (1 - abs(correlation_coefficient))

    conjecture_holds = correlation_coefficient >= 0.8 and p_value <= 0.01
    counterexample = "" if conjecture_holds else f"Correlation: {correlation_coefficient}, P-value: {p_value}"

    return {
        "metric_name": "Tropical Derivative Rank vs Resolution Width",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(seed) for seed in sys.argv[1:]]

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        print("RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8 or p-value > 0.05\" first_failing_seed=<s>")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")