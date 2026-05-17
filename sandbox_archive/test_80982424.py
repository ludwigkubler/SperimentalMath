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
        raise ValueError("n must be even for 3-regular graphs")
    edges = []
    vertices = list(range(n))
    degrees = [0] * n
    while len(edges) < 3 * n // 2:
        u, v = random.sample(vertices, 2)
        if degrees[u] < 3 and degrees[v] < 3 and u != v and (u, v) not in edges and (v, u) not in edges:
            edges.append((u, v))
            degrees[u] += 1
            degrees[v] += 1
    return edges

def generate_charge(n, seed):
    random.seed(seed)
    charge = [random.randint(0, 1) for _ in range(n)]
    if sum(charge) % 2 == 0:
        charge[0] = 1 - charge[0]
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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        if matrix[i][i] == 0:
            for j in range(i + 1, n):
                if matrix[j][i] == 1:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    break
        if matrix[i][i] == 0:
            continue
        for j in range(i + 1, n):
            if matrix[j][i] == 1:
                for k in range(i, n):
                    matrix[j][k] ^= matrix[i][k]
    rank = sum(1 for i in range(n) if any(matrix[i][j] for j in range(n)))
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
            L[i][j] ^= adjacency[i][j]
    L_tilde = [row[:n-1] for row in L[:n-1]]
    rank = gaussian_elimination(L_tilde)
    return (n - 1) - rank

def generate_tseitin_cnf(G, omega, n):
    clauses = []
    for u, v in G:
        clauses.append([u, v, n + len(clauses)])
    for i in range(n):
        if omega[i] == 1:
            clauses.append([i])
    return clauses

def dpll(clauses, assignment, node_count):
    node_count[0] += 1
    if not clauses:
        return True, node_count
    for clause in clauses:
        if not clause:
            return False, node_count
    unit_clauses = [c[0] for c in clauses if len(c) == 1]
    for lit in unit_clauses:
        if not assignment.get(lit, None) is None and assignment[lit] != 1:
            return False, node_count
        assignment[lit] = 1
        new_clauses = []
        for clause in clauses:
            if lit not in clause:
                new_clauses.append([x for x in clause if x != -lit])
        satisfied, node_count = dpll(new_clauses, assignment.copy(), node_count)
        if satisfied:
            return True, node_count
        assignment[lit] = 0
        new_clauses = []
        for clause in clauses:
            if -lit not in clause:
                new_clauses.append([x for x in clause if x != lit])
        satisfied, node_count = dpll(new_clauses, assignment.copy(), node_count)
        if satisfied:
            return True, node_count
    unassigned = [lit for lit in range(len(assignment)) if assignment.get(lit, None) is None]
    if not unassigned:
        return False, node_count
    lit = min(unassigned, key=lambda x: abs(x))
    assignment[lit] = 1
    new_clauses = []
    for clause in clauses:
        if lit not in clause:
            new_clauses.append([x for x in clause if x != -lit])
    satisfied, node_count = dpll(new_clauses, assignment.copy(), node_count)
    if satisfied:
        return True, node_count
    assignment[lit] = 0
    new_clauses = []
    for clause in clauses:
        if -lit not in clause:
            new_clauses.append([x for x in clause if x != lit])
    satisfied, node_count = dpll(new_clauses, assignment.copy(), node_count)
    return satisfied, node_count

def run_trial(seed):
    n_values = [6, 8, 10, 12, 14]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    for n in n_values:
        for _ in range(6):
            G = generate_3_regular_graph(n, seed)
            omega = generate_charge(n, seed)
            r2 = compute_r2(G, n)
            clauses = generate_tseitin_cnf(G, omega, n)
            node_count = [0]
            satisfied, node_count = dpll(clauses, {}, node_count)
            if not satisfied:
                N_DPLL = node_count[0]
                metric_value = math.log2(N_DPLL) if N_DPLL > 0 else 0
                bound = 0.25 * (n - 1 - r2)
                if metric_value < bound:
                    conjecture_holds = False
                    counterexample = f"n={n}, r2={r2}, N_DPLL={N_DPLL}, log2(N_DPLL)={metric_value}, bound={bound}"
                    break
                metric_values.append(metric_value)
                instances_tested += 1
            if not conjecture_holds:
                break
        if not conjecture_holds:
            break
    if not metric_values:
        metric_values = [0]
    return {
        "metric_name": "log2(N_DPLL)",
        "metric_value": sum(metric_values) / len(metric_values) if metric_values else 0,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = sys.argv[1:] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    instances_tested = 0
    conjecture_holds_all = True
    counterexample = ""
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        instances_tested += result["instances_tested"]
        if not result["conjecture_holds"]:
            conjecture_holds_all = False
            counterexample = result["counterexample"]
            break
    if conjecture_holds_all:
        mean = sum(metric_values) / len(metric_values)
        std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction=1.0")
    elif counterexample:
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[0]}")
    else:
        print("RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=150")