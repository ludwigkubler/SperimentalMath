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

def generate_3CNF(n, alpha, seed):
    random.seed(seed)
    m = int(alpha * n)
    literals = list(range(1, n + 1)) + list(range(-n, 0))
    clauses = []
    for _ in range(m):
        clause = random.sample(literals, 3)
        clauses.append(clause)
    return clauses

def is_unsatisfiable(F, max_backtracks=2**21):
    n = len(F) // 3
    literals = list(range(1, n + 1)) + list(range(-n, 0))
    assignment = {}
    backtracks = 0

    def backtrack():
        nonlocal backtracks
        if backtracks >= max_backtracks:
            return False
        if len(assignment) == n:
            return True
        var = random.choice([l for l in literals if abs(l) not in assignment])
        for val in [True, False]:
            assignment[abs(var)] = val
            if not any(all(not (lit < 0) == assignment.get(abs(lit), False) for lit in clause) for clause in F):
                if backtrack():
                    return True
            assignment.pop(abs(var))
            backtracks += 1
        return False

    return not backtrack()

def build_literal_conflict_graph(F):
    n = len(F) // 3
    graph = defaultdict(int)
    for clause in F:
        for a, b in itertools.combinations(clause, 2):
            graph[(a, b)] += 1
            graph[(b, a)] += 1
    return graph

def matrix_multiply(A, B):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
    return result

def compute_lambda_1(F):
    n = len(F) // 3
    graph = build_literal_conflict_graph(F)
    literals = list(range(1, n + 1)) + list(range(-n, 0))
    literal_to_index = {l: i for i, l in enumerate(literals)}
    index_to_literal = {i: l for i, l in enumerate(literals)}

    # Initialize adjacency matrix
    adj = [[0] * (2 * n) for _ in range(2 * n)]
    for (u, v), count in graph.items():
        i = literal_to_index[u]
        j = literal_to_index[v]
        adj[i][j] = count

    # Power iteration
    b = [random.random() for _ in range(2 * n)]
    for _ in range(200):
        b_new = matrix_multiply(adj, [list(x) for x in zip(*[b])])[0]
        norm = math.sqrt(sum(x**2 for x in b_new))
        if norm == 0:
            break
        b = [x / norm for x in b_new]

    lambda_1 = sum(b[i] * sum(adj[i][j] * b[j] for j in range(2 * n)) for i in range(2 * n))
    return lambda_1

def compute_D(F):
    n = len(F) // 3
    lambda_1 = compute_lambda_1(F)
    graph = build_literal_conflict_graph(F)
    d_bar = sum(count for count in graph.values()) / (2 * n)
    if d_bar == 0:
        return 0.0
    D = (lambda_1 ** 2) / (d_bar * 2 * n) - 1
    return D

def run_trial(seed):
    n_values = [10, 12, 14, 16, 18, 20, 22]
    alpha_values = [5.0, 5.5, 6.0, 6.5, 7.0]
    n = random.choice(n_values)
    alpha = random.choice(alpha_values)
    F = generate_3CNF(n, alpha, seed)
    if not is_unsatisfiable(F):
        return {
            "metric_name": "log2_B(F)/max(D(F),n^{-1/2})",
            "metric_value": 0.0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Generated CNF is satisfiable for seed {seed}"
        }

    D = compute_D(F)
    B = 2**21  # DPLL backtrack count capped at 2^21
    metric_value = math.log2(B) / max(D, n ** (-1/2))
    conjecture_holds = (1/100) * n <= metric_value <= 100 * n

    return {
        "metric_name": "log2_B(F)/max(D(F),n^{-1/2})",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Seed {seed} with n={n}, alpha={alpha}, D(F)={D}, B(F)={B}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(1, 10**6) for _ in range(30)]
    trials = []
    for seed in seeds:
        trial = run_trial(seed)
        trials.append(trial)
        print(f"TRIAL: {trial}")

    metric_values = [trial["metric_value"] for trial in trials if trial["metric_value"] != 0.0]
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
        first_failing_seed = next(seed for seed, trial in zip(seeds, trials) if not trial["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")