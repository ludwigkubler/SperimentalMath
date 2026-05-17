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

def generate_3_regular_graph(n, seed):
    random.seed(seed)
    if n % 2 != 0:
        raise ValueError("n must be even for a 3-regular graph")
    edges = []
    degrees = defaultdict(int)
    vertices = list(range(n))
    while len(edges) < 3 * n // 2:
        u, v = random.sample(vertices, 2)
        if u != v and degrees[u] < 3 and degrees[v] < 3 and (u, v) not in edges and (v, u) not in edges:
            edges.append((u, v))
            degrees[u] += 1
            degrees[v] += 1
    return edges

def generate_charge(n, seed):
    random.seed(seed)
    charge = [random.randint(0, 1) for _ in range(n)]
    if sum(charge) % 2 == 0:
        charge[random.randint(0, n-1)] ^= 1
    return charge

def matrix_multiply(A, B):
    n = len(A)
    m = len(B[0])
    p = len(B)
    result = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                result[i][j] ^= A[i][k] & B[k][j]
    return result

def matrix_rank(A):
    n = len(A)
    rank = 0
    for col in range(n):
        pivot = -1
        for row in range(rank, n):
            if A[row][col] == 1:
                pivot = row
                break
        if pivot == -1:
            continue
        A[rank], A[pivot] = A[pivot], A[rank]
        for row in range(n):
            if row != rank and A[row][col] == 1:
                for c in range(col, n):
                    A[row][c] ^= A[rank][c]
        rank += 1
    return rank

def compute_r2(G, n):
    L = [[0] * n for _ in range(n)]
    for u, v in G:
        L[u][v] ^= 1
        L[v][u] ^= 1
        L[u][u] ^= 1
        L[v][v] ^= 1
    L_tilde = [row[:n-1] for row in L[:n-1]]
    return (n - 1) - matrix_rank(L_tilde)

def tseitin_cnf(G, omega, n):
    clauses = []
    for u, v in G:
        clauses.append([u, v, n])
        clauses.append([u, v, n + 1])
        clauses.append([u, n, n + 1])
        clauses.append([v, n, n + 1])
    for i in range(n):
        if omega[i] == 1:
            clauses.append([i])
    return clauses

def dpll(clauses, assignment, decision_nodes):
    decision_nodes[0] += 1
    if all(any(lit in assignment for lit in clause) for clause in clauses):
        return True
    if any(all(-lit not in assignment for lit in clause) for clause in clauses):
        return False
    unassigned = [i for i in range(len(assignment)) if assignment[i] is None]
    if not unassigned:
        return False
    var = min(unassigned)
    for val in [True, False]:
        new_assignment = assignment.copy()
        new_assignment[var] = val
        if dpll(clauses, new_assignment, decision_nodes):
            return True
    return False

def run_trial(seed):
    n_sizes = [6, 8, 10, 12, 14]
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    instances_tested = 0

    for n in n_sizes:
        for _ in range(6):
            try:
                G = generate_3_regular_graph(n, seed)
                omega = generate_charge(n, seed)
                r2 = compute_r2(G, n)
                clauses = tseitin_cnf(G, omega, n)
                assignment = [None] * (n + 2)
                decision_nodes = [0]
                dpll(clauses, assignment, decision_nodes)
                N_DPLL = decision_nodes[0]
                if N_DPLL == 0:
                    continue
                metric_value = math.log2(N_DPLL) - 0.25 * (n - 1 - r2)
                metric_values.append(metric_value)
                instances_tested += 1
                if metric_value < 0:
                    conjecture_holds = False
                    counterexample = f"n={n}, seed={seed}, N_DPLL={N_DPLL}, r2={r2}"
                    break
            except Exception as e:
                continue
        if not conjecture_holds:
            break

    if not metric_values:
        return {
            "metric_name": "log2(N_DPLL) - 0.25*(n-1-r2)",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    mean_metric = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "log2(N_DPLL) - 0.25*(n-1-r2)",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample if not conjecture_holds else ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results if r["instances_tested"] > 0]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)

    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean:.4f} std={std:.4f} support_fraction={support_fraction:.4f}")
    else:
        counterexamples = [r["counterexample"] for r in results if not r["conjecture_holds"]]
        if counterexamples:
            first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample={counterexamples[0]} first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE reason=insufficient_support")