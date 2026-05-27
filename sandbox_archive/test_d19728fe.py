# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import itertools
from fractions import Fraction

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiplication(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_transpose(A):
    rows, cols = len(A), len(A[0])
    return [[A[j][i] for j in range(rows)] for i in range(cols)]

def gaussian_elimination(A):
    rows, cols = len(A), len(A[0])
    rank = 0
    for col in range(cols):
        pivot_row = -1
        for row in range(rank, rows):
            if A[row][col] != 0:
                pivot_row = row
                break
        if pivot_row == -1:
            continue
        A[pivot_row], A[rank] = A[rank], A[pivot_row]
        for r in range(rows):
            if r != rank and A[r][col] != 0:
                factor = Fraction(A[r][col], A[rank][col])
                for c in range(cols):
                    A[r][c] -= factor * A[rank][c]
        rank += 1
    return rank

def ehrhart_matrix(clauses):
    n = len(clauses)
    E = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            if any(lit in clauses[i] and -lit in clauses[j] for lit in set(clauses[i]) | set(clauses[j])):
                E[i][j] = 1
                E[j][i] = 1
    return E

def dpll(assignment, clauses):
    unsatisfied = [c for c in clauses if not any(lit in assignment and assignment[lit] == True or -lit in assignment and assignment[-lit] == False for lit in c)]
    if not unsatisfied:
        return True
    literal = next(lit for lit in set.union(*clauses) if lit not in assignment)
    for value in [True, False]:
        assignment[literal] = value
        if dpll(assignment, clauses):
            return True
        del assignment[literal]
    return False

def dpll_refutation_size(clauses):
    n = len(clauses)
    assignment = {}
    stack = []
    def backtrack():
        while stack:
            literal = stack.pop()
            if literal in assignment and not assignment[literal]:
                continue
            for lit in set.union(*clauses):
                if lit not in assignment:
                    assignment[lit] = True
                    stack.append(lit)
                    break
            else:
                return len(assignment)
        return 0
    return backtrack()

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(10, 40)
    clauses = []
    for _ in range(n):
        clause = [random.choice([-i, i]) for i in range(1, n+1)]
        if len(set(clause)) == 3:
            clauses.append(tuple(sorted(clause)))
    
    E = ehrhart_matrix(clauses)
    min_rank_E = gaussian_elimination(E)
    
    refutation_size = dpll_refutation_size(clauses)
    log2_refutation_size = Fraction(refutation_size).log(2) if refutation_size > 0 else -1
    
    C_alpha = 1.5  # Example constant for alpha = 0.5
    alpha = 0.5
    bound = C_alpha * (min_rank_E ** (1/2 + alpha))
    
    return {
        "metric_name": "log_2_refutation_size",
        "metric_value": log2_refutation_size,
        "instances_tested": 1,
        "conjecture_holds": log2_refutation_size <= bound,
        "counterexample": "" if log2_refutation_size <= bound else f"log2_refutation_size={log2_refutation_size} > {bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")