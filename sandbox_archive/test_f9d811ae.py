# auto-injected by SEC sandbox
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from fractions import Fraction

def matrix_multiply(A, B):
    n = len(A)
    result = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for k in range(n):
            if A[i][k] != 0:
                for j in range(n):
                    result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_transpose(M):
    return [list(row) for row in zip(*M)]

def matrix_norm(M):
    return math.sqrt(sum(sum(x*x for x in row) for row in M))

def power_iteration(M, num_iterations=200):
    n = len(M)
    b = [random.random() for _ in range(n)]
    for _ in range(num_iterations):
        b = matrix_multiply(M, [b])[0]
        norm = matrix_norm([b])
        if norm == 0:
            return 0.0
        b = [x / norm for x in b]
    return matrix_norm(matrix_multiply([b], matrix_multiply(M, [b]))[0])

def generate_3cnf(n, alpha, seed):
    random.seed(seed)
    m = int(alpha * n)
    variables = list(range(1, n+1))
    clauses = []
    for _ in range(m):
        clause_vars = random.sample(variables, 3)
        clause = []
        for var in clause_vars:
            if random.random() < 0.5:
                clause.append(var)
            else:
                clause.append(-var)
        clauses.append(clause)
    return clauses

def is_unsatisfiable(clauses, max_nodes=2**21):
    n = max(abs(lit) for clause in clauses for lit in clause)
    assignments = []
    nodes_explored = 0

    def backtrack():
        nonlocal nodes_explored
        if nodes_explored >= max_nodes:
            return False
        nodes_explored += 1

        if not clauses:
            return True

        clause = clauses[0]
        for lit in clause:
            if -lit not in assignments:
                assignments.append(lit)
                if backtrack():
                    return True
                assignments.pop()
        return False

    return not backtrack()

def build_literal_conflict_graph(clauses):
    n = max(abs(lit) for clause in clauses for lit in clause)
    graph = [[0 for _ in range(2*n)] for _ in range(2*n)]
    for clause in clauses:
        for i in range(3):
            for j in range(i+1, 3):
                lit1 = clause[i] + n if clause[i] > 0 else -clause[i]
                lit2 = clause[j] + n if clause[j] > 0 else -clause[j]
                graph[lit1-1][lit2-1] += 1
                graph[lit2-1][lit1-1] += 1
    return graph

def compute_d(F):
    n = max(abs(lit) for clause in F for lit in clause)
    graph = build_literal_conflict_graph(F)
    total_degree = sum(sum(row) for row in graph)
    num_edges = total_degree // 2
    return total_degree / (2 * n)

def run_trial(seed):
    n_values = [10, 12, 14, 16, 18, 20, 22]
    alpha_values = [5.0, 5.5, 6.0, 6.5, 7.0]
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for alpha in alpha_values:
            random.seed(seed)
            F = generate_3cnf(n, alpha, seed)
            if not is_unsatisfiable(F):
                continue

            graph = build_literal_conflict_graph(F)
            lambda1 = power_iteration(graph)
            d_bar = compute_d(F)
            D_F = (lambda1 ** 2) / (d_bar * 2 * n) - 1

            nodes_explored = 0
            def backtrack():
                nonlocal nodes_explored
                if nodes_explored >= 2**21:
                    return False
                nodes_explored += 1

                if not F:
                    return True

                clause = F[0]
                for lit in clause:
                    if -lit not in assignments:
                        assignments.append(lit)
                        if backtrack():
                            return True
                        assignments.pop()
                return False

            assignments = []
            if not backtrack():
                continue

            B_F = nodes_explored
            if B_F == 0:
                continue

            log_B_F = math.log2(B_F)
            max_D = max(D_F, n ** (-1/2))
            ratio = log_B_F / max_D

            if ratio < n / 100 or ratio > 100 * n:
                conjecture_holds = False
                counterexample = f"n={n}, alpha={alpha}, seed={seed}, D(F)={D_F}, B(F)={B_F}"

            metric_values.append(ratio)

    if not metric_values:
        return {
            "metric_name": "log_B_F / max(D(F), n^{-1/2})",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }

    mean_ratio = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "log_B_F / max(D(F), n^{-1/2})",
        "metric_value": mean_ratio,
        "instances_tested": len(metric_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trials = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        trials.append(trial)

    metric_values = [trial["metric_value"] for trial in trials if trial["instances_tested"] > 0]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)

    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)

    if all(trial["conjecture_holds"] for trial in trials):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        counterexample = next(trial["counterexample"] for trial in trials if not trial["conjecture_holds"])
        first_failing_seed = next(trial["seed"] for trial in trials if not trial["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")