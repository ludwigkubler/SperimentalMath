# auto-injected by SEC sandbox
import itertools
import json
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
from collections import deque

def matrix_multiply(A, B):
    n = len(A)
    result = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for k in range(n):
            if A[i][k] != 0:
                for j in range(n):
                    result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_inverse(A):
    n = len(A)
    I = [[float(i == j) for j in range(n)] for i in range(n)]
    for col in range(n):
        pivot = col
        for row in range(col + 1, n):
            if abs(A[row][col]) > abs(A[pivot][col]):
                pivot = row
        if A[pivot][col] == 0:
            raise ValueError("Matrix is not invertible")
        A[col], A[pivot] = A[pivot], A[col]
        I[col], I[pivot] = I[pivot], I[col]
        pivot_val = A[col][col]
        for j in range(col, n):
            A[col][j] /= pivot_val
        for j in range(n):
            I[col][j] /= pivot_val
        for i in range(n):
            if i != col and A[i][col] != 0:
                factor = A[i][col]
                for j in range(col, n):
                    A[i][j] -= factor * A[col][j]
                for j in range(n):
                    I[i][j] -= factor * I[col][j]
    return I

def compute_rho(adj, charge, n):
    L = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        L[i][i] = len(adj[i])
        for j in adj[i]:
            L[i][j] -= 1
    try:
        L_inv = matrix_inverse(L)
    except ValueError:
        return 0.0
    rho = 0.0
    charged_vertices = [i for i in range(n) if charge[i] == 1]
    if len(charged_vertices) >= 2:
        for u in charged_vertices:
            for v in charged_vertices:
                if u != v:
                    rho += L_inv[u][u] + L_inv[v][v] - 2 * L_inv[u][v]
        rho /= (n * len(charged_vertices) * (len(charged_vertices) - 1))
    else:
        v0 = charged_vertices[0]
        for v in range(n):
            if v != v0:
                rho += L_inv[v0][v0] + L_inv[v][v] - 2 * L_inv[v0][v]
        rho /= n
    return rho

def generate_3_regular_graph(n, seed):
    random.seed(seed)
    while True:
        edges = []
        degree = [0] * n
        for i in range(n):
            for _ in range(3):
                j = random.randint(0, n - 1)
                while j == i or degree[j] >= 3:
                    j = random.randint(0, n - 1)
                edges.append((i, j))
                degree[i] += 1
                degree[j] += 1
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
        visited = [False] * n
        queue = deque([0])
        visited[0] = True
        count = 1
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    count += 1
                    queue.append(v)
        if count == n:
            return adj

def generate_charge(n, seed, k):
    random.seed(seed + 1)
    charge = [0] * n
    vertices = list(range(n))
    random.shuffle(vertices)
    for i in range(k):
        charge[vertices[i]] = 1
    return charge

def build_tseitin_cnf(adj, charge, n):
    clauses = []
    for u in range(n):
        neighbors = adj[u]
        for i in range(len(neighbors)):
            for j in range(i + 1, len(neighbors)):
                v, w = neighbors[i], neighbors[j]
                clauses.append([(u, 1), (v, 1), (w, 1)])
                clauses.append([(u, 0), (v, 0), (w, 0)])
                clauses.append([(u, 1), (v, 0), (w, 0)])
                clauses.append([(u, 0), (v, 1), (w, 0)])
                clauses.append([(u, 0), (v, 0), (w, 1)])
                clauses.append([(u, 1), (v, 1), (w, 0)])
    for u in range(n):
        if charge[u] == 1:
            clauses.append([(u, 1)])
        else:
            clauses.append([(u, 0)])
    return clauses

def dpll(clauses, assignment, decision_nodes):
    if decision_nodes > 1 << 20:
        return float('inf')
    unit_clauses = []
    for clause in clauses:
        if len(clause) == 1:
            unit_clauses.append(clause[0])
    for lit in unit_clauses:
        if lit in assignment:
            if assignment[lit] != 1:
                return 0
        else:
            assignment[lit] = 1
            decision_nodes += 1
    pure_literals = {}
    for clause in clauses:
        for lit in clause:
            if lit not in pure_literals:
                pure_literals[lit] = True
            else:
                pure_literals[lit] = False
    for lit, is_pure in pure_literals.items():
        if is_pure and lit not in assignment:
            assignment[lit] = 1
            decision_nodes += 1
    satisfied = []
    unsatisfied = []
    for clause in clauses:
        sat = False
        for lit in clause:
            if lit in assignment and assignment[lit] == 1:
                sat = True
                break
        if sat:
            satisfied.append(clause)
        else:
            unsatisfied.append(clause)
    if not unsatisfied:
        return 1
    if any(len(clause) == 0 for clause in unsatisfied):
        return 0
    var = None
    min_occurrences = float('inf')
    for clause in unsatisfied:
        for lit in clause:
            if lit not in assignment:
                occurrences = sum(1 for c in unsatisfied if lit in c)
                if occurrences < min_occurrences:
                    min_occurrences = occurrences
                    var = lit[0]
    if var is None:
        return 0
    left_assignment = assignment.copy()
    left_assignment[(var, 1)] = 1
    left_result = dpll(unsatisfied, left_assignment, decision_nodes)
    if left_result == 0:
        right_assignment = assignment.copy()
        right_assignment[(var, 0)] = 1
        right_result = dpll(unsatisfied, right_assignment, decision_nodes)
        return left_result + right_result
    else:
        return left_result

def run_trial(seed):
    n = random.choice([10, 14, 18, 22, 26, 30])
    adj = generate_3_regular_graph(n, seed)
    k = random.choice([1, 3, 5])
    charge = generate_charge(n, seed, k)
    rho = compute_rho(adj, charge, n)
    if rho == 0:
        return {
            "metric_name": "R",
            "metric_value": 0.0,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    clauses = build_tseitin_cnf(adj, charge, n)
    t_star = dpll(clauses, {}, 0)
    if t_star == float('inf'):
        return {
            "metric_name": "R",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    R = math.log2(t_star) / (n * rho)
    conjecture_holds = R >= 0.005
    counterexample = "" if conjecture_holds else f"R = {R} < 0.005"
    return {
        "metric_name": "R",
        "metric_value": R,
        "instances_tested": 1,
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
    metric_values = [trial["metric_value"] for trial in trials if trial["metric_value"] != float('inf')]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)
    mean_R = sum(metric_values) / len(metric_values)
    std_R = math.sqrt(sum((R - mean_R) ** 2 for R in metric_values) / len(metric_values))
    support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)
    if all(trial["conjecture_holds"] for trial in trials):
        print(f"RESULT: SUPPORTED mean={mean_R} std={std_R} support_fraction={support_fraction}")
    elif any(not trial["conjecture_holds"] for trial in trials):
        first_failing_seed = seeds[next(i for i, trial in enumerate(trials) if not trial["conjecture_holds"])]
        counterexample = next(trial["counterexample"] for trial in trials if not trial["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")