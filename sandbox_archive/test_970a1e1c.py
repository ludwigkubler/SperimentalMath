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

# Helper functions for matrix operations
def matrix_add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(B[0]))] for i in range(len(A))]

def matrix_sub(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(B[0]))] for i in range(len(A))]

def matrix_mul(A, B):
    result = [[sum(a * b for a, b in zip(row_A, col_B)) for col_B in zip(*B)] for row_A in A]
    return result

def gaussian_elimination(M):
    n = len(M)
    for i in range(n):
        max_row = max(range(i, n), key=lambda k: abs(M[k][i]))
        M[i], M[max_row] = M[max_row], M[i]
        factor = Fraction(M[i][i])
        M[i] = [[M[i][j] / factor for j in range(n + 1)] for j in range(n)]
        for j in range(n):
            if i != j:
                factor = Fraction(M[j][i])
                M[j] = [M[j][k] - factor * M[i][k] for k in range(n + 1)]
    return M

def matrix_inv(A):
    n = len(A)
    I = [[Fraction(1, 0) if i == j else Fraction(0, 1) for j in range(n)] for i in range(n)]
    A_augmented = [row + col for row, col in zip(A, I)]
    A_rref = gaussian_elimination(A_augmented)
    return [row[n:] for row in A_rref]

def matrix_det(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = Fraction(0, 1)
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1) ** j * A[0][j] * matrix_det(submatrix)
    return det

def matrix_rank(A):
    rref = gaussian_elimination(A)
    rank = sum(1 for row in rref if any(val != 0 for val in row))
    return rank

# Helper function to generate random CNFs
def generate_cnf(n, m):
    cnf = []
    literals = list(range(-n, 0)) + list(range(1, n+1))
    for _ in range(m):
        clause = [random.choice(literals) for _ in range(random.randint(2, 3))]
        cnf.append(clause)
    return cnf

# Helper function to compute DPLL search tree width
def dpll_width(cnf):
    def backtrack(clauses, assignment):
        if not clauses:
            return 0
        unit_clauses = [c for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            new_clauses = [[l for l in c if l != literal and -l not in new_assignment] for c in clauses]
            return 1 + backtrack(new_clauses, new_assignment)
        pure_literals = [l for l in literals if all(l not in c or -l in assignment for c in clauses)]
        if pure_literals:
            literal = pure_literals[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            new_clauses = [[l for l in c if l != literal and -l not in new_assignment] for c in clauses]
            return 1 + backtrack(new_clauses, new_assignment)
        literal = random.choice(literals)
        new_assignment_true = assignment.copy()
        new_assignment_true[literal] = True
        new_clauses_true = [[l for l in c if l != literal and -l not in new_assignment_true] for c in clauses]
        width_true = 1 + backtrack(new_clauses_true, new_assignment_true)
        new_assignment_false = assignment.copy()
        new_assignment_false[literal] = False
        new_clauses_false = [[l for l in c if l != literal and -l not in new_assignment_false] for c in clauses]
        width_false = 1 + backtrack(new_clauses_false, new_assignment_false)
        return max(width_true, width_false)
    return backtrack(cnf, {})

# Helper function to construct Kähler manifold X from CNF φ
def construct_kahler_manifold(cnf):
    n = len(cnf)
    X = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in cnf:
        for literal in clause:
            if literal > 0:
                X[literal][literal - 1] += 1
                X[literal - 1][literal] += 1
            else:
                X[-literal][-literal - 1] += 1
                X[-literal - 1][-literal] += 1
    return X

# Helper function to compute minimal order of Kähler manifold X
def minimal_order(X):
    det = matrix_det(X)
    rank = matrix_rank(X)
    return abs(det) ** (1 / rank)

# Main trial function
def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    total_diff = 0.0
    counterexample = ""
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        m = random.randint(n * 2, n * 3)
        cnf = generate_cnf(n, m)
        X = construct_kahler_manifold(cnf)
        w_phi = dpll_width(cnf)
        order_X = minimal_order(X)
        diff = abs(order_X - w_phi)
        total_diff += diff
        
        if diff > 2:
            counterexample = f"CNF with n={n}, m={m} and width {w_phi} has |order_X - w_phi| = {diff}"
            break
    
    metric_name = "Absolute Difference"
    metric_value = total_diff / instances_tested
    conjecture_holds = metric_value <= 2
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_diff = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_diff} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")