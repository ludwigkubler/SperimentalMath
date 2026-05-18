# auto-injected by SEC sandbox
import itertools
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import json
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
    n = len(A)
    norm = 0.0
    for i in range(n):
        for j in range(n):
            norm += A[i][j] ** 2
    return math.sqrt(norm)

def power_iteration(A, max_iter=200):
    n = len(A)
    b_k = [random.random() for _ in range(n)]
    for _ in range(max_iter):
        b_k1 = [0.0] * n
        for i in range(n):
            for j in range(n):
                b_k1[i] += A[i][j] * b_k[j]
        norm = matrix_norm([b_k1])
        if norm == 0:
            break
        b_k = [x / norm for x in b_k1]
    lambda_1 = 0.0
    for i in range(n):
        for j in range(n):
            lambda_1 += b_k[i] * A[i][j] * b_k[j]
    return lambda_1

def generate_3cnf(n, alpha):
    m = int(alpha * n)
    literals = list(range(1, n + 1)) + list(range(-n, 0))
    clauses = []
    for _ in range(m):
        clause = random.sample(literals, 3)
        clauses.append(clause)
    return clauses

def is_unsatisfiable(clauses):
    n = len(clauses[0]) // 2 if clauses else 0
    if n == 0:
        return False
    assignments = {}
    for clause in clauses:
        for lit in clause:
            if lit not in assignments:
                assignments[lit] = random.choice([True, False])
    for clause in clauses:
        satisfied = any(assignments.get(abs(lit), False) == (lit > 0) for lit in clause)
        if not satisfied:
            return True
    return False

def build_literal_conflict_graph(clauses):
    n = len(clauses[0]) // 2 if clauses else 0
    if n == 0:
        return [], 0
    graph = defaultdict(int)
    edges = []
    for clause in clauses:
        for i in range(3):
            for j in range(i + 1, 3):
                lit1, lit2 = clause[i], clause[j]
                if lit1 > lit2:
                    lit1, lit2 = lit2, lit1
                edge = (lit1, lit2)
                edges.append(edge)
                graph[edge] += 1
    return edges, n

def compute_d(F):
    edges, n = build_literal_conflict_graph(F)
    if n == 0:
        return 0.0
    total_degree = sum(count for count in edges)
    return total_degree / (2 * n)

def compute_lambda_1(F):
    edges, n = build_literal_conflict_graph(F)
    if n == 0:
        return 0.0
    adj = [[0 for _ in range(2 * n)] for _ in range(2 * n)]
    for (u, v), count in edges:
        adj[u + n - 1][v + n - 1] += count
        adj[v + n - 1][u + n - 1] += count
    return power_iteration(adj)

def compute_D(F):
    lambda_1 = compute_lambda_1(F)
    d = compute_d(F)
    n = len(F[0]) // 2 if F else 0
    if n == 0 or d == 0:
        return 0.0
    return (lambda_1 ** 2) / (d * 2 * n) - 1

def dpll(F, max_nodes=2**21):
    n = len(F[0]) // 2 if F else 0
    if n == 0:
        return 0
    assignments = {}
    backtracks = 0

    def backtrack():
        nonlocal backtracks
        backtracks += 1
        if backtracks > max_nodes:
            return None
        if len(assignments) == n:
            return assignments
        unassigned = [lit for lit in range(1, n + 1) if lit not in assignments and -lit not in assignments]
        if not unassigned:
            return assignments
        lit = random.choice(unassigned)
        for val in [True, False]:
            assignments[lit] = val
            result = backtrack()
            if result is not None:
                return result
            del assignments[lit]
        return None

    return backtracks

def run_trial(seed):
    random.seed(seed)
    n_values = [10, 12, 14, 16, 18, 20, 22]
    alpha_values = [5.0, 5.5, 6.0, 6.5, 7.0]
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    instances_tested = 0

    for n in n_values:
        for alpha in alpha_values:
            for _ in range(30):
                F = generate_3cnf(n, alpha)
                if not is_unsatisfiable(F):
                    continue
                D = compute_D(F)
                B = dpll(F)
                if B == 0:
                    continue
                log_B = math.log2(B)
                max_term = max(D, n ** (-1/2))
                ratio = log_B / max_term
                if ratio < n / 100 or ratio > 100 * n:
                    conjecture_holds = False
                    counterexample = f"n={n}, alpha={alpha}, seed={seed}, D={D}, B={B}"
                    break
                metric_values.append(ratio)
                instances_tested += 1
            if not conjecture_holds:
                break
        if not conjecture_holds:
            break

    if not metric_values:
        return {
            "metric_name": "log₂ B(F) / max(D(F), n^{-1/2})",
            "metric_value": 0.0,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }

    mean_metric = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "log₂ B(F) / max(D(F), n^{-1/2})",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trials = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {json.dumps({'seed': seed, **trial})}")
        trials.append(trial)

    metric_values = [trial["metric_value"] for trial in trials if trial["metric_value"] != 0.0]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)

    if all(trial["conjecture_holds"] for trial in trials):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not trial["conjecture_holds"] for trial in trials):
        first_failing_seed = next(trial["seed"] for trial in trials if not trial["conjecture_holds"])
        counterexample = next(trial["counterexample"] for trial in trials if not trial["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")