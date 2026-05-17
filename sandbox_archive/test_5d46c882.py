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
        if degrees[u] < 3 and degrees[v] < 3 and u != v and (u, v) not in edges and (v, u) not in edges:
            edges.append((u, v))
            degrees[u] += 1
            degrees[v] += 1
    return edges

def generate_odd_weight_charge(n):
    omega = [random.randint(0, 1) for _ in range(n)]
    if sum(omega) % 2 == 0:
        omega[random.randint(0, n-1)] ^= 1
    return omega

def matrix_mult(A, B):
    return [[sum(a * b for a, b in zip(row, col)) for col in zip(*B)] for row in A]

def matrix_add(A, B):
    return [[a + b for a, b in zip(row, col)] for row, col in zip(A, B)]

def matrix_sub(A, B):
    return [[a - b for a, b in zip(row, col)] for row, col in zip(A, B)]

def matrix_transpose(A):
    return [list(row) for row in zip(*A)]

def gaussian_elimination_mod2(matrix):
    n = len(matrix)
    for i in range(n):
        if matrix[i][i] == 0:
            for j in range(i+1, n):
                if matrix[j][i] == 1:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    break
        if matrix[i][i] == 0:
            continue
        for j in range(i+1, n):
            if matrix[j][i] == 1:
                matrix[j] = [x ^ y for x, y in zip(matrix[j], matrix[i])]
    rank = sum(1 for i in range(n) if any(matrix[i]))
    return rank

def compute_r2(G, n):
    if n <= 1:
        return 0
    adj = defaultdict(list)
    for u, v in G:
        adj[u].append(v)
        adj[v].append(u)
    L = [[0] * n for _ in range(n)]
    for u in range(n):
        L[u][u] = len(adj[u])
        for v in adj[u]:
            L[u][v] = 1
    L_tilde = [row[:n-1] for row in L[:n-1]]
    rank = gaussian_elimination_mod2(L_tilde)
    return (n - 1) - rank

def tseitin_cnf(G, omega, n):
    clauses = []
    for u, v in G:
        clauses.append([u, v, n])
        clauses.append([-u, -v, n])
        clauses.append([u, -v, -n])
        clauses.append([-u, v, -n])
    for i in range(n):
        if omega[i] == 1:
            clauses.append([i])
        else:
            clauses.append([-i])
    return clauses

def dpll(clauses, assignment, node_count):
    unit_clauses = [c for c in clauses if len(c) == 1]
    while unit_clauses:
        literal = unit_clauses.pop()[0]
        if literal in assignment:
            if assignment[literal] != (literal > 0):
                return False, node_count
            continue
        assignment[abs(literal)] = literal > 0
        new_clauses = []
        for clause in clauses:
            if literal in clause:
                continue
            if -literal in clause:
                new_clause = [l for l in clause if l != -literal]
                if not new_clause:
                    return False, node_count
                if len(new_clause) == 1:
                    unit_clauses.append(new_clause)
                else:
                    new_clauses.append(new_clause)
            else:
                new_clauses.append(clause)
        clauses = new_clauses
        unit_clauses = [c for c in clauses if len(c) == 1]
    if not clauses:
        return True, node_count
    unassigned = [i for i in range(1, len(assignment) + 1) if i not in assignment]
    if not unassigned:
        return False, node_count
    literal = unassigned[0]
    node_count += 1
    for value in [True, False]:
        new_assignment = assignment.copy()
        new_assignment[literal] = value
        satisfied, node_count = dpll(clauses, new_assignment, node_count)
        if satisfied:
            return True, node_count
    return False, node_count

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
            _, node_count = dpll(clauses, {}, 0)
            if node_count == 0:
                continue
            log2_node_count = math.log2(node_count)
            bound = 0.25 * (n - 1 - r2)
            if log2_node_count < bound:
                conjecture_holds = False
                counterexample = f"n={n}, r2={r2}, log2_node_count={log2_node_count}, bound={bound}"
                break
            metric_values.append(log2_node_count - bound)
            instances_tested += 1
        if not conjecture_holds:
            break
    return {
        "metric_name": "slack",
        "metric_value": sum(metric_values) / len(metric_values) if metric_values else 0,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        result["seed"] = seed
        print(f"TRIAL: {result}")
        results.append(result)
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={r['seed']}")
                break