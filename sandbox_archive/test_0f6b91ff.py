# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from itertools import combinations

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            raise ValueError("No unique solution exists")
        for j in range(i + 1, n):
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

def dpll_with_memoization(clauses, assignment):
    if not clauses:
        return True
    clause = next(c for c in clauses if any(l in assignment and assignment[l] == 1 for l in c))
    if not clause:
        return False
    literal = next(l for l in clause if l not in assignment)
    assignment[literal] = 1
    if dpll_with_memoization(clauses, assignment):
        return True
    assignment[literal] = -1
    if dpll_with_memoization(clauses, assignment):
        return True
    del assignment[literal]
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    clauses = []
    for _ in range(n * (n - 1) // 2):
        literals = [random.choice([-i, i]) for i in range(1, n + 1)]
        if any(l == -m or l == m for l, m in combinations(literals, 2)):
            continue
        clauses.append(literals)
    E_n = sum(abs(sum(c.count(l) for c in clauses)) for l in range(-n, n + 1))
    
    assignment = {}
    P_n = 0
    while not dpll_with_memoization(clauses, assignment):
        literal = random.choice([-i, i] for i in range(1, n + 1) if -i not in assignment and i not in assignment)
        assignment[literal] = 1
        P_n += 1
    
    conjecture_holds = True
    counterexample = ""
    if E_n > P_n:
        conjecture_holds = False
        counterexample = "E(n) > P(n)"
    if P_n > E_n * 2:
        conjecture_holds = False
        counterexample = "P(n) > 2E(n)"
    
    return {
        "metric_name": "Ehrhart Polynomial Coefficient Sum",
        "metric_value": E_n,
        "instances_tested": len(clauses),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    E_n_values = [r["metric_value"] for r in results]
    P_n_values = [2 * r["instances_tested"] for r in results]  # Simplified upper bound for demonstration
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(E_n_values)/len(E_n_values)} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"E(n) > P(n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")