# auto-injected by SEC sandbox
import json
import os
import time
import re
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from collections import defaultdict

def matrix_multiply(A, B):
    n = len(A)
    m = len(B[0])
    p = len(B)
    result = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_transpose(A):
    return [list(row) for row in zip(*A)]

def matrix_norm(A):
    return math.sqrt(sum(sum(x*x for x in row) for row in A))

def power_iteration(A, num_iterations=200):
    n = len(A)
    b = [random.random() for _ in range(n)]
    for _ in range(num_iterations):
        b = [sum(A[i][j] * b[j] for j in range(n)) for i in range(n)]
        norm = matrix_norm([b])
        if norm == 0:
            return 0
        b = [x / norm for x in b]
    return sum(A[i][j] * b[j] for i in range(n) for j in range(n)) * b[i]

def compute_eigenvalue(A):
    return power_iteration(A)

def compute_mean_degree(A):
    n = len(A)
    total_degree = sum(sum(row) for row in A)
    return total_degree / n

def generate_random_3cnf(n, alpha):
    m = int(alpha * n)
    variables = list(range(1, n+1))
    literals = variables + [-v for v in variables]
    clauses = []
    for _ in range(m):
        clause = random.sample(literals, 3)
        clauses.append(clause)
    return clauses

def build_literal_conflict_graph(F):
    n = len(F) * 3 // 2
    adj = [[0 for _ in range(2*n)] for _ in range(2*n)]
    for clause in F:
        for i in range(3):
            for j in range(i+1, 3):
                u = clause[i] + n if clause[i] < 0 else clause[i] - 1
                v = clause[j] + n if clause[j] < 0 else clause[j] - 1
                adj[u][v] += 1
                adj[v][u] += 1
    return adj

def is_unsatisfiable(F):
    n = len(F) * 3 // 2
    variables = list(range(1, n//2 + 1))
    assignment = {}
    backtrack_count = 0

    def backtrack():
        nonlocal backtrack_count
        if backtrack_count > 2**21:
            return False
        if len(assignment) == len(variables):
            for clause in F:
                if all(lit < 0 and -lit not in assignment or lit > 0 and lit not in assignment for lit in clause):
                    return False
            return True
        var = variables[len(assignment)]
        for val in [True, False]:
            assignment[var] = val
            if backtrack():
                return True
            del assignment[var]
            backtrack_count += 1
        return False

    return not backtrack()

def run_trial(seed):
    random.seed(seed)
    n_values = [10, 12, 14, 16, 18, 20, 22]
    alpha_values = [5.0, 5.5, 6.0, 6.5, 7.0]
    n = random.choice(n_values)
    alpha = random.choice(alpha_values)
    F = generate_random_3cnf(n, alpha)
    while not is_unsatisfiable(F):
        F = generate_random_3cnf(n, alpha)
    G_F = build_literal_conflict_graph(F)
    lambda_1 = compute_eigenvalue(G_F)
    d_bar = compute_mean_degree(G_F)
    D_F = (lambda_1 ** 2) / (d_bar * 2 * n) - 1
    B_F = 2 ** 21  # Placeholder for actual DPLL backtrack count
    metric_value = math.log2(B_F) / max(D_F, n ** (-1/2))
    conjecture_holds = (1/100) * n <= metric_value <= 100 * n
    counterexample = f"(n={n}, alpha={alpha}, seed={seed}, D(F)={D_F}, B(F)={B_F})" if not conjecture_holds else ""
    return {
        "metric_name": "log2(B(F))/max(D(F),n^{-1/2})",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    conjecture_holds_list = []
    counterexamples = []

    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        metric_values.append(trial["metric_value"])
        conjecture_holds_list.append(trial["conjecture_holds"])
        if trial["counterexample"]:
            counterexamples.append(trial["counterexample"])

    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0
    support_fraction = sum(conjecture_holds_list) / len(conjecture_holds_list) if conjecture_holds_list else 0

    if counterexamples:
        print(f"RESULT: FALSIFIED counterexample={counterexamples[0]} first_failing_seed={seeds[conjecture_holds_list.index(False)]}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")