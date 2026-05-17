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

def generate_3_regular_graph(n):
    if n % 2 != 0:
        raise ValueError("n must be even for 3-regular graphs")
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

def generate_odd_weight_charge(n):
    omega = [random.randint(0, 1) for _ in range(n)]
    if sum(omega) % 2 == 0:
        omega[random.randint(0, n-1)] ^= 1
    return omega

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
    adjacency = [[0] * n for _ in range(n)]
    for u, v in G:
        adjacency[u][v] ^= 1
        adjacency[v][u] ^= 1
    L = [[0] * n for _ in range(n)]
    for i in range(n):
        L[i][i] = sum(adjacency[i])
        for j in range(n):
            if i != j:
                L[i][j] = adjacency[i][j]
    L_tilde = [row[:-1] for row in L[:-1]]
    rank = matrix_rank(L_tilde)
    return (n - 1) - rank

def tseitin_cnf(G, omega, n):
    clauses = []
    for u, v in G:
        clauses.append([u, v, n + len(clauses)])
        clauses.append([u, v, n + len(clauses)])
    for i in range(n):
        if omega[i] == 1:
            clauses.append([i])
        else:
            clauses.append([i, i])
    return clauses

def dpll(clauses, assignment, decision_nodes):
    decision_nodes[0] += 1
    if all(any(literal in assignment for literal in clause) for clause in clauses):
        return True
    if any(all(literal not in assignment and -literal not in assignment for literal in clause) for clause in clauses):
        return False
    unassigned = [i for i in range(len(assignment)) if i not in assignment and -i not in assignment]
    if not unassigned:
        return False
    literal = unassigned[0]
    for value in [True, False]:
        new_assignment = assignment.copy()
        new_assignment[literal] = value
        if dpll(clauses, new_assignment, decision_nodes):
            return True
    return False

def run_trial(seed):
    random.seed(seed)
    n_sizes = [6, 8, 10, 12, 14]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    for n in n_sizes:
        for _ in range(6):
            G = generate_3_regular_graph(n)
            omega = generate_odd_weight_charge(n)
            r2 = compute_r2(G, n)
            clauses = tseitin_cnf(G, omega, n)
            decision_nodes = [0]
            dpll(clauses, {}, decision_nodes)
            N_DPLL = decision_nodes[0]
            if N_DPLL == 0:
                continue
            log2_N_DPLL = math.log2(N_DPLL)
            bound = 0.25 * (n - 1 - r2)
            if log2_N_DPLL < bound:
                conjecture_holds = False
                counterexample = f"n={n}, r2={r2}, log2_N_DPLL={log2_N_DPLL}, bound={bound}"
                return {
                    "metric_name": "log2_N_DPLL",
                    "metric_value": log2_N_DPLL,
                    "instances_tested": instances_tested + 1,
                    "conjecture_holds": conjecture_holds,
                    "counterexample": counterexample
                }
            metric_values.append(log2_N_DPLL)
            instances_tested += 1
    if conjecture_holds:
        mean_metric = sum(metric_values) / len(metric_values)
        return {
            "metric_name": "log2_N_DPLL",
            "metric_value": mean_metric,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }
    else:
        return {
            "metric_name": "log2_N_DPLL",
            "metric_value": 0.0,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    metric_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    if metric_values:
        mean = sum(metric_values) / len(metric_values)
        std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    else:
        mean, std = 0.0, 0.0
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seeds[results.index(r)]}")
                break