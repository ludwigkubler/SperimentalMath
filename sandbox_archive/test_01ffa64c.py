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
    rank = 0
    for i in range(m):
        if rank == n:
            break
        pivot_row = i
        while pivot_row < m and A[pivot_row][i] == 0:
            pivot_row += 1
        if pivot_row == m:
            continue
        A[i], A[pivot_row] = A[pivot_row], A[i]
        for j in range(m):
            if j != i:
                factor = -A[j][i] / A[i][i]
                for k in range(n):
                    if k < i:
                        A[j][k] += factor * A[i][k]
                    elif k > i:
                        A[j][k] -= factor * A[i][k]
        rank += 1
    return rank

def matrix_multiplication(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1) ** j * A[0][j] * determinant(submatrix)
    return det

def rank(matrix):
    return gaussian_elimination(matrix)

def create_tropical_matrix(clauses, variables):
    m = len(clauses)
    n = len(variables)
    matrix = [[0 for _ in range(n)] for _ in range(m)]
    for i, clause in enumerate(clauses):
        for literal in clause:
            if literal[0] == 'x':
                var_index = int(literal[1:]) - 1
                matrix[i][var_index] = max(matrix[i][var_index], literal[2:])
            elif literal[0] == '~':
                var_index = int(literal[1:]) - 1
                matrix[i][var_index] = max(matrix[i][var_index], literal[3:])
    return matrix

def dpll_depth(clauses, variables):
    def solve(clauses, assignment):
        if not clauses:
            return True
        clause = next((c for c in clauses if any(l in assignment for l in c)), None)
        if not clause:
            return False
        literal = next(l for l in clause if l in assignment)
        if literal[0] == '~':
            literal = literal[1:]
            negated = True
        else:
            negated = False
        var_index = int(literal[1:]) - 1
        if assignment[var_index] != negated:
            return solve(clauses, assignment)
        assignment[var_index] = not negated
        if solve(clauses, assignment):
            return True
        assignment[var_index] = negated
        return False
    return len(solve(clauses, [False] * len(variables)))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    variables = {f'x{i+1}': i for i in range(n)}
    clauses = []
    for _ in range(m):
        clause = []
        num_literals = random.randint(1, n)
        for _ in range(num_literals):
            literal = random.choice(['x', '~']) + str(random.randint(1, n)) + str(random.randint(0, 9))
            if literal not in clause:
                clause.append(literal)
        clauses.append(clause)
    tropical_matrix = create_tropical_matrix(clauses, variables)
    dpll_depth_value = dpll_depth(clauses, variables)
    rank_value = rank(tropical_matrix)
    metric_value = rank_value / math.log(dpll_depth_value + 1) if dpll_depth_value > 0 else float('inf')
    instances_tested = 1
    conjecture_holds = metric_value <= 2.0
    counterexample = "" if conjecture_holds else f"rank={rank_value}, depth={dpll_depth_value}"
    return {
        "metric_name": "Rank/Log(DPLL Depth)",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"rank/log(depth) > 2\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")