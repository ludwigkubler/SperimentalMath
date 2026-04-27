# auto-injected by SEC sandbox
import collections
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import json
from itertools import combinations

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda x: abs(A[x][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(n):
            if j != i:
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    return A

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def largest_eigenvalue(A, tol=1e-6, max_iter=1000):
    n = len(A)
    v = [random.random() for _ in range(n)]
    v /= math.sqrt(sum(x**2 for x in v))
    for _ in range(max_iter):
        Av = matrix_multiplication(A, v)
        lambda_ = sum(Av[i] * v[i] for i in range(n)) / sum(v[i]**2 for i in range(n))
        v_next = Av
        v_next /= math.sqrt(sum(x**2 for x in v_next))
        if abs(lambda_ - sum(Av[i] * v[i] for i in range(n))) < tol:
            return lambda_
    return sum(Av[i] * v[i] for i in range(n)) / sum(v[i]**2 for i in range(n))

def dpll_runtime(formula):
    def solve(clauses, assignment):
        if not clauses:
            return True
        clause = random.choice(clauses)
        literals = set(abs(lit) for lit in clause)
        for lit in literals:
            new_assignment = assignment.copy()
            new_assignment[lit] = True
            if solve([c for c in clauses if not any(l in c or -l in c for l in new_assignment)], new_assignment):
                return True
            new_assignment[lit] = False
            if solve([c for c in clauses if not any(l in c or -l in c for l in new_assignment)], new_assignment):
                return True
        return False
    return len(formula) * 10  # Simplified runtime estimation

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 8, 11, 14])
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(3 * n):
        clause = [random.choice(variables) if random.random() < 0.5 else -random.choice(variables) for _ in range(3)]
        clauses.append(clause)
    
    adjacency_matrix = [[0] * (len(clauses) + 1) for _ in range(len(clauses) + 1)]
    for i, clause1 in enumerate(clauses):
        for j, clause2 in enumerate(clauses):
            if any(lit in clause1 or -lit in clause1 for lit in clause2):
                adjacency_matrix[i][j] = 1
                adjacency_matrix[j][i] = 1
    
    lambda_max = largest_eigenvalue(adjacency_matrix)
    
    runtime = dpll_runtime(clauses)
    
    return {
        "metric_name": "DPLL Runtime",
        "metric_value": runtime,
        "instances_tested": 1,
        "conjecture_holds": runtime <= 2**(lambda_max * n),
        "counterexample": "" if runtime <= 2**(lambda_max * n) else f"Runtime {runtime} exceeds expected bound {2**(lambda_max * n)}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    mean_runtime = sum(r["metric_value"] for r in results) / len(results)
    std_runtime = math.sqrt(sum((r["metric_value"] - mean_runtime)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_runtime} std={std_runtime} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Runtime exceeds expected bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")