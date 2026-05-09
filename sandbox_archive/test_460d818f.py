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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def matrix_multiply(A, B):
    m, k, n = len(A), len(B[0]), len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def dpll(clauses, assignment):
    if not clauses:
        return True
    if any(all(c[i] == 0 for c in clause) for i in range(len(assignment))):
        return False
    var = next(i for i, val in enumerate(assignment) if val is None)
    for value in [True, False]:
        new_assignment = assignment[:]
        new_assignment[var] = value
        new_clauses = []
        for clause in clauses:
            if any(c[var] == 0 for c in clause):
                continue
            new_clause = [c for c in clause if c != (var + 1) * -value and c != var + 1]
            if not new_clause:
                return False
            new_clauses.append(new_clause)
        if dpll(new_clauses, new_assignment):
            return True
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    rho = random.uniform(1.2, 2.5)
    num_clauses = math.ceil(n * rho / 3)
    clauses = []
    for _ in range(num_clauses):
        clause = [random.choice([-i - 1, i]) for i in range(1, n + 1)]
        random.shuffle(clause)
        clauses.append(clause)
    
    # Construct the clause graph
    adjacency_matrix = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in clauses:
        for var in clause:
            if var > 0:
                adjacency_matrix[0][var] += 1
                adjacency_matrix[var][0] += 1
            else:
                u, v = abs(var), abs(clause[(i + 1) % len(clause)])
                adjacency_matrix[u][v] += 1
                adjacency_matrix[v][u] += 1
    
    # Compute Betti number (edges - vertices + connected components)
    edges = sum(sum(row) for row in adjacency_matrix) // 2
    vertices = n + 1
    visited = [False] * (n + 1)
    
    def dfs(v):
        stack = [v]
        while stack:
            u = stack.pop()
            if not visited[u]:
                visited[u] = True
                for i in range(1, n + 2):
                    if adjacency_matrix[u][i] > 0 and not visited[i]:
                        stack.append(i)
    
    dfs(0)
    connected_components = sum(not v for v in visited)
    betti_1 = edges - vertices + connected_components
    
    # Run DPLL to measure tree size
    assignment = [None] * (n + 1)
    dpll_size = len(dpll(clauses, assignment))
    
    result = {
        "metric_name": "Betti_1 * DPLL_size",
        "metric_value": betti_1 * dpll_size,
        "instances_tested": 1,
        "conjecture_holds": 0.8 * n <= betti_1 * dpll_size <= 1.2 * n,
        "counterexample": "" if result["conjecture_holds"] else f"n={n}, Betti_1*{dpll_size}={betti_1*dpll_size}"
    }
    
    return result

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")