# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(n):
            if j != i:
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    return A

def solve_linear_system(A, b):
    m, n = len(A), len(A[0])
    A_aug = [row + [b[i]] for i, row in enumerate(A)]
    A_rref = gaussian_elimination(A_aug)
    x = [0] * n
    for i in range(m-1, -1, -1):
        if A_rref[i][i] == 0:
            continue
        x[i] = A_rref[i][-1]
        for j in range(i+1, m):
            x[i] -= A_rref[i][j] * x[j]
        x[i] /= A_rref[i][i]
    return x

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def random_3_regular_graph(n):
    V = list(range(n))
    E = []
    while len(E) < n:
        u, v = random.sample(V, 2)
        if (u, v) not in E and (v, u) not in E and u != v:
            degree_u = sum(1 for e in E if e[0] == u or e[1] == u)
            degree_v = sum(1 for e in E if e[0] == v or e[1] == v)
            if degree_u < 3 and degree_v < 3:
                E.append((u, v))
    return V, E

def tseitin_formula(G, sigma):
    V, E = G
    n = len(V)
    literals = {v: f'x{v}' for v in V}
    neg_literals = {v: f'~x{v}' for v in V}
    clauses = []
    for u, v in E:
        clauses.append([literals[u], neg_literals[v]])
        clauses.append([neg_literals[u], literals[v]])
    for v in V:
        if sigma[v] == 1:
            clauses.append([literals[v]])
        else:
            clauses.append([neg_literals[v]])
    return clauses

def dpll(clauses, assignment):
    if not clauses:
        return True
    unit_clause = next((c for c in clauses if len(c) == 1), None)
    if unit_clause is not None:
        literal = unit_clause[0]
        value = literal[0] != '~'
        var = int(literal[2:])
        assignment[var] = value
        new_clauses = [c for c in clauses if (value and literal in c) or (not value and neg_literal in c)]
        return dpll(new_clauses, assignment)
    pure_literal = next((l for l in literals if all(l not in clause for clause in clauses)), None)
    if pure_literal is not None:
        value = pure_literal[0] != '~'
        var = int(pure_literal[2:])
        assignment[var] = value
        new_clauses = [c for c in clauses if (value and literal in c) or (not value and neg_literal in c)]
        return dpll(new_clauses, assignment)
    var = random.choice(list(assignment.keys()))
    value = not assignment[var]
    assignment[var] = value
    new_clauses = [c for c in clauses if (value and literal in c) or (not value and neg_literal in c)]
    if dpll(new_clauses, assignment):
        return True
    del assignment[var]
    assignment[var] = not value
    new_clauses = [c for c in clauses if (value and literal in c) or (not value and neg_literal in c)]
    if dpll(new_clauses, assignment):
        return True
    del assignment[var]
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([8, 10, 12, 14, 16])
    V, E = random_3_regular_graph(n)
    sigma = {v: random.randint(0, 1) for v in V}
    G = (V, E)
    
    # Compute ν(G)
    A = [[0] * n for _ in range(n)]
    for u, v in E:
        A[u][v] = A[v][u] = 1
    b = [0] * n
    for i in range(n):
        b[i] = sum(A[i])
    x = solve_linear_system(A, b)
    phi_lp = min(sum(x) / n**2, 1)
    nu = n**2 * phi_lp
    
    # Build Tseitin formula and run DPLL
    clauses = tseitin_formula(G, sigma)
    assignment = {}
    result = dpll(clauses, assignment)
    
    # Compute log₂(T_R)
    if result:
        T_R = sum(1 for k in range(n) if assignment[k])
    else:
        T_R = 0
    
    # Check conditions
    conjecture_holds = True
    counterexample = ""
    if nu >= 40 and math.log2(T_R) < nu / 40 - 5:
        conjecture_holds = False
        counterexample = "log₂(T_R) < ν/40 - 5"
    elif nu > 8 and (G[1] == [(0, 3), (1, 4), (2, 5)] or G[1] == [(0, 3), (1, 4), (2, 5), (6, 7), (8, 9), (10, 11), (12, 13), (14, 15)]):
        conjecture_holds = False
        counterexample = "ν > 8 on non-expander family"
    
    return {
        "metric_name": "log₂(T_R)",
        "metric_value": math.log2(T_R),
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r["counterexample"] == "log₂(T_R) < ν/40 - 5" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"] == "log₂(T_R) < ν/40 - 5")
        print(f"RESULT: FALSIFIED counterexample=\"log₂(T_R) < ν/40 - 5\" first_failing_seed={first_failing_seed}")
    elif any(r["counterexample"] == "ν > 8 on non-expander family" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"] == "ν > 8 on non-expander family")
        print(f"RESULT: FALSIFIED counterexample=\"ν > 8 on non-expander family\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")