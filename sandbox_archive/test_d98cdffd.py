# auto-injected by SEC sandbox
import itertools
import json
import os
import time
import re
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
from collections import defaultdict, deque
from fractions import Fraction

def matrix_mult(A, B):
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
    identity = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    for col in range(n):
        pivot = col
        for row in range(col + 1, n):
            if abs(A[row][col]) > abs(A[pivot][col]):
                pivot = row
        if pivot != col:
            A[col], A[pivot] = A[pivot], A[col]
            identity[col], identity[pivot] = identity[pivot], identity[col]
        if A[col][col] == 0:
            raise ValueError("Matrix is singular")
        pivot_val = A[col][col]
        for j in range(col, n):
            A[col][j] = Fraction(A[col][j], pivot_val)
        for j in range(n):
            identity[col][j] = Fraction(identity[col][j], pivot_val)
        for i in range(n):
            if i != col and A[i][col] != 0:
                factor = A[i][col]
                for j in range(col, n):
                    A[i][j] -= factor * A[col][j]
                for j in range(n):
                    identity[i][j] -= factor * identity[col][j]
    return identity

def graph_laplacian(adj, n):
    L = [[0 for _ in range(n)] for _ in range(n)]
    for u in range(n):
        L[u][u] = len(adj[u])
        for v in adj[u]:
            L[u][v] -= 1
    return L

def effective_resistance(L, u, v):
    n = len(L)
    if u == v:
        return 0
    L_sub = [row[:v] + row[v+1:] for row in (L[:u] + L[u+1:])]
    L_sub_inv = matrix_inverse(L_sub)
    R_eff = L_sub_inv[u][u] + L_sub_inv[v][v] - 2 * L_sub_inv[u][v]
    return R_eff

def generate_3_regular_graph(n):
    if n % 2 != 0:
        raise ValueError("n must be even for a 3-regular graph")
    edges = []
    stubs = [i // 3 for i in range(3 * n)]
    random.shuffle(stubs)
    while stubs:
        u = stubs.pop()
        v = stubs.pop()
        if u != v and (u, v) not in edges and (v, u) not in edges:
            edges.append((u, v))
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    if not is_connected(adj, n):
        return generate_3_regular_graph(n)
    return adj

def is_connected(adj, n):
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
    return count == n

def generate_charge(n, k):
    if k > n:
        raise ValueError("k must be <= n")
    charge = [0] * n
    vertices = list(range(n))
    random.shuffle(vertices)
    for i in range(k):
        charge[vertices[i]] = 1
    return charge

def build_tseitin_cnf(adj, charge, n):
    cnf = []
    for u in range(n):
        neighbors = adj[u]
        if len(neighbors) != 3:
            raise ValueError("Graph is not 3-regular")
        v1, v2, v3 = neighbors
        cnf.append([u, v1, v2, v3])
        cnf.append([u, v1, -v2, -v3])
        cnf.append([u, -v1, v2, -v3])
        cnf.append([u, -v1, -v2, v3])
    for u in range(n):
        if charge[u] == 1:
            cnf.append([u])
    return cnf

def dpll_solver(cnf, max_nodes=2**20):
    def unit_propagate(clauses, assignment):
        changed = True
        while changed:
            changed = False
            for clause in clauses:
                unassigned = [lit for lit in clause if abs(lit) not in assignment]
                if len(unassigned) == 1:
                    lit = unassigned[0]
                    val = (lit > 0)
                    if abs(lit) in assignment and assignment[abs(lit)] != val:
                        return False, {}
                    assignment[abs(lit)] = val
                    changed = True
        return True, assignment

    def pure_literal_elimination(clauses, assignment):
        literals = set()
        for clause in clauses:
            for lit in clause:
                literals.add(lit)
        pure_literals = set()
        for lit in literals:
            if -lit not in literals:
                pure_literals.add(lit)
        for lit in pure_literals:
            assignment[abs(lit)] = (lit > 0)
        return [clause for clause in clauses if not any(abs(lit) in assignment for lit in clause)]

    def shallowest_variable(clauses, assignment):
        variables = set()
        for clause in clauses:
            for lit in clause:
                if abs(lit) not in assignment:
                    variables.add(abs(lit))
        if not variables:
            return None
        return min(variables)

    def dpll(clauses, assignment, nodes):
        if nodes >= max_nodes:
            return None, nodes
        clauses = [clause for clause in clauses if not any(assignment.get(abs(lit), None) == (lit < 0) for lit in clause)]
        if not clauses:
            return assignment, nodes
        if any(not clause for clause in clauses):
            return None, nodes
        clauses = pure_literal_elimination(clauses, assignment)
        success, new_assignment = unit_propagate(clauses, assignment)
        if not success:
            return None, nodes
        assignment.update(new_assignment)
        var = shallowest_variable(clauses, assignment)
        if var is None:
            return assignment, nodes
        for val in [True, False]:
            new_assignment = assignment.copy()
            new_assignment[var] = val
            result, new_nodes = dpll(clauses, new_assignment, nodes + 1)
            if result is not None:
                return result, new_nodes
        return None, nodes

    assignment, nodes = dpll(cnf, {}, 0)
    return nodes

def run_trial(seed):
    random.seed(seed)
    n_sizes = [10, 14, 18, 22, 26, 30]
    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_sizes:
        if n % 2 != 0:
            continue
        adj = generate_3_regular_graph(n)
        k = random.choice([1, 3, 5])
        if k > n:
            continue
        charge = generate_charge(n, k)
        L = graph_laplacian(adj, n)
        rho = 0
        if k == 1:
            v0 = charge.index(1)
            for v in range(n):
                if v != v0:
                    R_eff = effective_resistance(L, v0, v)
                    rho += R_eff
            rho /= n
        else:
            charged_vertices = [v for v in range(n) if charge[v] == 1]
            for u in charged_vertices:
                for v in charged_vertices:
                    if u != v:
                        R_eff = effective_resistance(L, u, v)
                        rho += R_eff
            rho /= n
        cnf = build_tseitin_cnf(adj, charge, n)
        t_star = dpll_solver(cnf)
        if t_star is None:
            t_star = 2**20
        R = math.log2(t_star) / (n * rho)
        metric_values.append(R)
        instances_tested += 1
        if R < 0.005:
            conjecture_holds = False
            counterexample = f"n={n}, seed={seed}, R={R}"

    if not metric_values:
        return {
            "metric_name": "R",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }

    mean_R = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "R",
        "metric_value": mean_R,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = sys.argv[1:] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    trials = []
    for seed in seeds:
        trial = run_trial(int(seed))
        print(f"TRIAL: {trial}")
        trials.append(trial)

    metric_values = [trial["metric_value"] for trial in trials if trial["metric_value"] > 0]
    instances_tested = sum(trial["instances_tested"] for trial in trials)
    conjecture_holds = all(trial["conjecture_holds"] for trial in trials)

    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
    else:
        mean_R = sum(metric_values) / len(metric_values)
        std_R = math.sqrt(sum((R - mean_R) ** 2 for R in metric_values) / len(metric_values))
        support_fraction = sum(1 for trial in trials if trial["conjecture_holds"]) / len(trials)

        if conjecture_holds and mean_R >= 0.02:
            print(f"RESULT: SUPPORTED mean={mean_R} std={std_R} support_fraction={support_fraction}")
        else:
            counterexamples = [trial["counterexample"] for trial in trials if not trial["conjecture_holds"]]
            if counterexamples:
                first_failing_seed = next(trial["seed"] for trial in trials if not trial["conjecture_holds"])
                print(f"RESULT: FALSIFIED counterexample={counterexamples[0]} first_failing_seed={first_failing_seed}")
            else:
                print("RESULT: INCONCLUSIVE reason=insufficient_support")