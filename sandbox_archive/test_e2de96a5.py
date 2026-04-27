# auto-injected by SEC sandbox
import itertools
import collections
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
import json

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def solve_linear_system(A, b):
    n = len(A)
    A_b = [row + [b[i]] for i, row in enumerate(A)]
    A_b = gaussian_elimination(A_b)
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (A_b[i][-1] - sum(A_b[i][j] * x[j] for j in range(i + 1, n))) / A_b[i][i]
    return x

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def random_3cnf(n, m):
    clauses = []
    variables = set(range(1, n + 1))
    while len(clauses) < m:
        clause = set()
        for _ in range(3):
            var = random.choice(list(variables))
            if random.choice([True, False]):
                clause.add(-var)
            else:
                clause.add(var)
        if len(clause) == 3 and all(len(c & clause) <= 1 for c in clauses):
            clauses.append(clause)
    return clauses

def evaluate_f_F(f_F, assignment):
    n = len(assignment)
    value = 0
    for i in range(1 << n):
        binary_assignment = [(-1 if (i >> j) & 1 else 1) for j in range(n)]
        if all(binary_assignment[var - 1] == f_F[var] for var in assignment):
            value += 1
    return value

def compute_stab_1_3(f_F, rho=1/3, samples=4000):
    n = len(f_F)
    total = 0
    for _ in range(samples):
        x = [random.choice([-1, 1]) for _ in range(n)]
        y = [x[i] if random.random() < rho else -x[i] for i in range(n)]
        total += f_F[x[0]] * f_F[y[0]]
    return total / samples

def dpll(F, assignment=[]):
    n = len(F)
    if not F:
        return 1
    var = next(var for var in range(1, n + 1) if any(var in clause or -var in clause for clause in F))
    count = 0
    for value in [-1, 1]:
        new_assignment = assignment + [var]
        new_F = [clause for clause in F if not (value == 1 and var in clause or value == -1 and -var in clause)]
        count += dpll(new_F, new_assignment)
    return count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [8, 10, 12, 14, 16, 18, 20]
    densities = [3.0, 4.26, 5.0]
    results = []
    
    for n in n_values:
        for alpha in densities:
            m = int(n * alpha)
            F = random_3cnf(n, m)
            f_F = {tuple(sorted([var if var > 0 else -var for var in clause])): 1 for clause in F}
            S_F = compute_stab_1_3(f_F)
            L_F = dpll(F)
            
            instances_tested = 1
            conjecture_holds = True
            counterexample = ""
            
            if len(F) > 0:
                expected_L_F = 2**n * S_F / (3 * m)
                slack = abs(L_F - expected_L_F)
                if L_F < expected_L_F and slack > 3 * math.sqrt(S_F / samples):
                    conjecture_holds = False
                    counterexample = f"Unsatisfiable: L(F)={L_F}, expected >= {expected_L_F}"
            else:
                expected_L_F = 2**n * (1 - 9*S_F/m)
                slack = abs(L_F - expected_L_F)
                if L_F > expected_L_F and slack > 3 * math.sqrt(S_F / samples):
                    conjecture_holds = False
                    counterexample = f"Satisfiable: L(F)={L_F}, expected <= {expected_L_F}"
            
            results.append({
                "metric_name": "L(F)",
                "metric_value": L_F,
                "instances_tested": instances_tested,
                "conjecture_holds": conjecture_holds,
                "counterexample": counterexample
            })
    
    return {
        "seed": seed,
        "results": results
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    all_results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": result}))
        all_results.extend(result["results"])
    
    mean_L_F = sum(r["metric_value"] for r in all_results) / len(all_results)
    std_dev_L_F = math.sqrt(sum((r["metric_value"] - mean_L_F)**2 for r in all_results) / len(all_results))
    support_fraction = sum(1 for r in all_results if r["conjecture_holds"]) / len(all_results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_L_F} std={std_dev_L_F} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in all_results):
        first_failing_seed = next(r["seed"] for r in all_results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")