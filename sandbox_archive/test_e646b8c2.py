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
    stubs = list(range(n)) * 3
    while stubs:
        u = random.choice(stubs)
        stubs.remove(u)
        v = random.choice([x for x in stubs if x != u])
        stubs.remove(v)
        edges.append((u, v))
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj

def is_connected(adj):
    if not adj:
        return True
    visited = set()
    stack = [next(iter(adj))]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            stack.extend(adj[node])
    return len(visited) == len(adj)

def generate_charge(n, k, seed):
    random.seed(seed)
    if k > n:
        raise ValueError("k must be <= n")
    vertices = list(range(n))
    random.shuffle(vertices)
    charge = [0] * n
    for i in range(k):
        charge[vertices[i]] = 1
    return charge

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

def matrix_inverse(A):
    n = len(A)
    identity = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        identity[i][i] = 1
    augmented = [row[:] for row in A]
    for i in range(n):
        augmented[i].extend(identity[i])
    for col in range(n):
        max_row = col
        for row in range(col + 1, n):
            if abs(augmented[row][col]) > abs(augmented[max_row][col]):
                max_row = row
        augmented[col], augmented[max_row] = augmented[max_row], augmented[col]
        if augmented[col][col] == 0:
            raise ValueError("Matrix is singular")
        for row in range(n):
            if row != col:
                factor = augmented[row][col] / augmented[col][col]
                for c in range(2 * n):
                    augmented[row][c] -= factor * augmented[col][c]
    inverse = [row[n:] for row in augmented]
    return inverse

def compute_resistance(adj, charge):
    n = len(adj)
    L = [[0 for _ in range(n)] for _ in range(n)]
    for u in adj:
        L[u][u] = len(adj[u])
        for v in adj[u]:
            L[u][v] = -1
    L_pseudo = matrix_inverse(L)
    R_eff = 0
    support = [i for i, x in enumerate(charge) if x == 1]
    if len(support) >= 2:
        for u, v in itertools.combinations(support, 2):
            R_eff += L_pseudo[u][u] + L_pseudo[v][v] - 2 * L_pseudo[u][v]
        R_eff /= len(support) * (len(support) - 1)
    else:
        v0 = support[0]
        for v in range(n):
            if v != v0:
                R_eff += L_pseudo[v0][v0] + L_pseudo[v][v] - 2 * L_pseudo[v0][v]
        R_eff /= n - 1
    return R_eff

def build_tseitin_cnf(adj, charge):
    clauses = []
    for u in adj:
        for v in adj[u]:
            if u < v:
                clauses.append([(u, 1), (v, 1), (u + v, 0)])
                clauses.append([(u, 0), (v, 0), (u + v, 0)])
                clauses.append([(u, 1), (v, 0), (u + v, 1)])
                clauses.append([(u, 0), (v, 1), (u + v, 1)])
    for u in range(len(adj)):
        if charge[u] == 1:
            clauses.append([(u, 1)])
    return clauses

def dpll_solve(clauses, max_nodes=2**20):
    def unit_propagate(clauses, assignment):
        changed = True
        while changed:
            changed = False
            for clause in clauses:
                unassigned = [lit for lit in clause if lit[0] not in assignment]
                if len(unassigned) == 1:
                    lit = unassigned[0]
                    assignment[lit[0]] = lit[1]
                    changed = True
                    break
        return assignment

    def pure_literal_elimination(clauses, assignment):
        literals = set()
        for clause in clauses:
            for lit in clause:
                literals.add((lit[0], lit[1]))
        pure_literals = set()
        for lit in literals:
            if (lit[0], 1 - lit[1]) not in literals:
                pure_literals.add(lit)
        for lit in pure_literals:
            assignment[lit[0]] = lit[1]
        return assignment

    def shallowest_variable(clauses, assignment):
        variables = set()
        for clause in clauses:
            for lit in clause:
                if lit[0] not in assignment:
                    variables.add(lit[0])
        if not variables:
            return None
        return min(variables)

    def dpll(clauses, assignment, nodes):
        if nodes >= max_nodes:
            return None, nodes
        assignment = unit_propagate(clauses, assignment)
        assignment = pure_literal_elimination(clauses, assignment)
        for clause in clauses:
            satisfied = False
            for lit in clause:
                if lit[0] in assignment and assignment[lit[0]] == lit[1]:
                    satisfied = True
                    break
            if not satisfied:
                return None, nodes
        if all(len(adj[u]) == sum(1 for lit in assignment if lit[0] == u) for u in adj):
            return assignment, nodes
        var = shallowest_variable(clauses, assignment)
        if var is None:
            return assignment, nodes
        for value in [0, 1]:
            new_assignment = assignment.copy()
            new_assignment[var] = value
            result, nodes = dpll(clauses, new_assignment, nodes + 1)
            if result is not None:
                return result, nodes
        return None, nodes

    assignment, nodes = dpll(clauses, {}, 0)
    return nodes

def run_trial(seed):
    random.seed(seed)
    n_sizes = [10, 14, 18, 22, 26, 30]
    n = random.choice(n_sizes)
    k = random.choice([1, 3, 5])
    adj = None
    for _ in range(100):
        adj = generate_3_regular_graph(n, seed + _)
        if is_connected(adj):
            break
    if not is_connected(adj):
        return {
            "metric_name": "R",
            "metric_value": 0.0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Failed to generate connected graph"
        }
    charge = generate_charge(n, k, seed)
    try:
        rho = compute_resistance(adj, charge)
        if rho <= 0:
            return {
                "metric_name": "R",
                "metric_value": 0.0,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "Invalid resistance value"
            }
        cnf = build_tseitin_cnf(adj, charge)
        t_star = dpll_solve(cnf)
        if t_star is None:
            t_star = 2**20
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
    except Exception as e:
        return {
            "metric_name": "R",
            "metric_value": 0.0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": str(e)
        }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [42, 17, 23, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157]
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    metric_values = [trial["metric_value"] for trial in results if trial["metric_value"] > 0]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)
    mean_R = sum(metric_values) / len(metric_values)
    std_R = math.sqrt(sum((x - mean_R) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for trial in results if trial["conjecture_holds"]) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_R} std={std_R} support_fraction={support_fraction}")
    else:
        counterexamples = [trial["counterexample"] for trial in results if not trial["conjecture_holds"]]
        if counterexamples:
            first_failing_seed = seeds[results.index(next(trial for trial in results if not trial["conjecture_holds"]))]
            print(f"RESULT: FALSIFIED counterexample={counterexamples[0]} first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE reason=insufficient_support")