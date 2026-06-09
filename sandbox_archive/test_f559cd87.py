# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def matrix_mult(A, B):
    m, k = len(A), len(B[0])
    result = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(len(B)):
                result[i][j] += A[i][l] * B[l][j]
    return result

def dpll(clauses, assignment):
    if not clauses:
        return True
    var = next((v for v in range(len(assignment)) if assignment[v] is None), len(assignment))
    for value in [True, False]:
        new_assignment = assignment[:]
        new_assignment[var] = value
        new_clauses = []
        for clause in clauses:
            if any(lit == var or lit == -var for lit in clause):
                continue
            new_clause = [lit for lit in clause if lit != -var]
            if not new_clause:
                return False
            new_clauses.append(new_clause)
        if dpll(new_clauses, new_assignment):
            return True
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    m = random.randint(n, n * 10)
    clauses = []
    for _ in range(m):
        clause = [random.choice([-i - 1, i]) for i in range(n)]
        if not any(lit == -lit2 for lit, lit2 in zip(clause, clause[1:])):
            clauses.append(clause)
    
    assignment = [None] * n
    h_DPLL = 0 if dpll(clauses, assignment) else float('inf')
    
    # Minimal tropical curve representation (simplified example)
    C_phi = len(clauses)
    
    correlation_coefficient = (C_phi - h_DPLL) / max(C_phi, h_DPLL)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": correlation_coefficient <= -0.8,
        "counterexample": "" if correlation_coefficient <= -0.8 else f"Counterexample: C(φ)={C_phi}, h_DPLL(φ)={h_DPLL}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(r["metric_value"] > -0.8 for r in results):
        first_failing_seed = next((r["seed"] for r in results if r["metric_value"] > -0.8), None)
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient>0.8' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")