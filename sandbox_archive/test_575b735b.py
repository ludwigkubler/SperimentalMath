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

def generate_3_regular_graph(n, seed):
    random.seed(seed)
    if n % 2 != 0:
        raise ValueError("n must be even for 3-regular graph")
    edges = []
    stubs = [i for i in range(n) for _ in range(3)]
    while stubs:
        u = random.choice(stubs)
        stubs.remove(u)
        v = random.choice([x for x in stubs if x != u])
        stubs.remove(v)
        edges.append((u, v))
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    for neighbors in adj:
        if len(neighbors) != 3:
            raise ValueError("Graph is not 3-regular")
    return adj

def generate_charge(n, seed, k):
    random.seed(seed + n)
    charge = [0] * n
    vertices = list(range(n))
    random.shuffle(vertices)
    for i in range(k):
        charge[vertices[i]] = 1
    return charge

def matrix_multiply(A, B):
    n = len(A)
    result = [[0] * len(B[0]) for _ in range(n)]
    for i in range(n):
        for j in range(len(B[0])):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_add(A, B):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = A[i][j] + B[i][j]
    return result

def matrix_subtract(A, B):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = A[i][j] - B[i][j]
    return result

def matrix_transpose(A):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = A[j][i]
    return result

def matrix_inverse(A):
    n = len(A)
    I = [[0] * n for _ in range(n)]
    for i in range(n):
        I[i][i] = 1
    AI = [row[:] for row in A]
    for col in range(n):
        pivot = AI[col][col]
        if pivot == 0:
            raise ValueError("Matrix is not invertible")
        for i in range(n):
            AI[col][i] /= pivot
            I[col][i] /= pivot
        for row in range(n):
            if row != col and AI[row][col] != 0:
                factor = AI[row][col]
                for i in range(n):
                    AI[row][i] -= factor * AI[col][i]
                    I[row][i] -= factor * I[col][i]
    return I

def compute_laplacian(adj, n):
    L = [[0] * n for _ in range(n)]
    for i in range(n):
        L[i][i] = len(adj[i])
        for j in adj[i]:
            L[i][j] -= 1
    return L

def compute_effective_resistance(L_inv, u, v):
    n = len(L_inv)
    if u == v:
        return 0.0
    return L_inv[u][u] + L_inv[v][v] - 2 * L_inv[u][v]

def compute_rho(adj, charge, n):
    L = compute_laplacian(adj, n)
    L_inv = matrix_inverse(L)
    rho = 0.0
    support = [i for i, c in enumerate(charge) if c == 1]
    if len(support) == 1:
        v0 = support[0]
        for v in range(n):
            if v != v0:
                rho += compute_effective_resistance(L_inv, v0, v)
        rho /= n
    else:
        for u in support:
            for v in support:
                if u != v:
                    rho += compute_effective_resistance(L_inv, u, v)
        rho /= (n * len(support))
    return rho

def build_tseitin_cnf(adj, charge, n):
    cnf = []
    for u in range(n):
        neighbors = adj[u]
        if len(neighbors) != 3:
            raise ValueError("Graph is not 3-regular")
        x_u = f"x{u}"
        x_v1, x_v2, x_v3 = f"x{neighbors[0]}", f"x{neighbors[1]}", f"x{neighbors[2]}"
        cnf.append([x_u, x_v1, x_v2])
        cnf.append([x_u, x_v1, x_v3])
        cnf.append([x_u, x_v2, x_v3])
        cnf.append([x_u, x_v1, x_v2, x_v3])
    for u in range(n):
        if charge[u] == 1:
            cnf.append([f"x{u}"])
    return cnf

def dpll_solve(cnf, max_nodes=2**20):
    def unit_propagate(clauses, assignment):
        changed = True
        while changed:
            changed = False
            for clause in clauses[:]:
                if len(clause) == 1:
                    lit = clause[0]
                    if lit not in assignment:
                        assignment[lit] = True
                        changed = True
                        clauses = [c for c in clauses if lit not in c]
                        clauses = [[l for l in c if l != f"-{lit}"] for c in clauses]
        return clauses, assignment

    def pure_literal_elimination(clauses, assignment):
        literals = set()
        for clause in clauses:
            for lit in clause:
                literals.add(lit)
        pure = set()
        for lit in literals:
            if f"-{lit}" not in literals:
                pure.add(lit)
        for lit in pure:
            assignment[lit] = True
        clauses = [c for c in clauses if not any(lit in c for lit in pure)]
        return clauses, assignment

    def shallowest_variable(clauses):
        variables = set()
        for clause in clauses:
            for lit in clause:
                variables.add(lit.replace("-", ""))
        if not variables:
            return None
        return min(variables, key=lambda v: sum(1 for c in clauses if v in c or f"-{v}" in c))

    def dpll(clauses, assignment, nodes):
        if nodes >= max_nodes:
            return None
        clauses, assignment = unit_propagate(clauses, assignment)
        if not clauses:
            return assignment
        if any(not clause for clause in clauses):
            return None
        clauses, assignment = pure_literal_elimination(clauses, assignment)
        if not clauses:
            return assignment
        if any(not clause for clause in clauses):
            return None
        var = shallowest_variable(clauses)
        if var is None:
            return assignment
        for val in [True, False]:
            new_assignment = assignment.copy()
            new_assignment[var] = val
            new_clauses = [c for c in clauses if not (var in c and not val) and not (f"-{var}" in c and val)]
            result = dpll(new_clauses, new_assignment, nodes + 1)
            if result is not None:
                return result
        return None

    assignment = {}
    return dpll(cnf, assignment, 0)

def run_trial(seed):
    n_values = [10, 14, 18, 22, 26, 30]
    instances_tested = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        adj = generate_3_regular_graph(n, seed)
        for k in [1, 3, 5]:
            if k > n:
                continue
            charge = generate_charge(n, seed, k)
            rho = compute_rho(adj, charge, n)
            cnf = build_tseitin_cnf(adj, charge, n)
            assignment = dpll_solve(cnf)
            if assignment is None:
                t_star = 2**20
            else:
                t_star = len(assignment)
            R = math.log2(t_star) / (n * rho)
            metric_values.append(R)
            instances_tested += 1
            if R < 0.005:
                conjecture_holds = False
                counterexample = f"n={n}, k={k}, R={R}, t_star={t_star}, rho={rho}"

    metric_value = sum(metric_values) / len(metric_values) if metric_values else 0.0
    return {
        "metric_name": "R",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(seed) for seed in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)

    metric_values = [trial["metric_value"] for trial in results]
    mean_metric = sum(metric_values) / len(metric_values) if metric_values else 0.0
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values)) if metric_values else 0.0
    support_fraction = sum(1 for trial in results if trial["conjecture_holds"]) / len(results) if results else 0.0

    if any(not trial["conjecture_holds"] for trial in results):
        first_failing_seed = next(trial["seed"] for trial in results if not trial["conjecture_holds"])
        counterexample = next(trial["counterexample"] for trial in results if not trial["conjecture_holds"])
        print(f'RESULT: FALSIFIED counterexample="{counterexample}" first_failing_seed={first_failing_seed}')
    elif support_fraction >= 0.8:
        print(f'RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}')
    else:
        print('RESULT: INCONCLUSIVE reason=insufficient_support')