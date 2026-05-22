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
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]

        factor = Fraction(A[i][i])
        for j in range(i, n):
            A[i][j] /= factor
        b[i] /= factor

        for k in range(n):
            if k != i:
                factor = Fraction(A[k][i])
                for j in range(i, n):
                    A[k][j] -= factor * A[i][j]
                b[k] -= factor * b[i]

    return [b[i] for i in range(n)]

def matrix_multiplication(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = [[Fraction(0) for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def is_expander(G, delta=0.5):
    n = len(G)
    degrees = [sum(1 for _ in G[v]) for v in G]
    avg_degree = sum(degrees) / n
    if avg_degree < 2 * delta:
        return False
    for degree in degrees:
        if degree < delta * (n - 1):
            return False
    return True

def tseitin_formula(n):
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    for v in variables:
        clauses.append([v])
        clauses.append([-v])
    for i in range(2, n+1):
        a, b = random.sample(variables[:i], 2)
        c = f'x{i+1}'
        clauses.append([a, b, -c])
        clauses.append([-a, -b, c])
        clauses.append([-a, c])
        clauses.append([-b, c])
    return variables, clauses

def resolution_length(G):
    n = len(G)
    variables = [f'x{i}' for i in range(1, n+1)]
    unit_clauses = {c for c in G if len(c) == 1}
    while unit_clauses:
        u = next(iter(unit_clauses))
        unit_clauses.remove(u)
        v = u[0]
        for clause in G:
            if v in clause and -v not in clause:
                new_clause = [c for c in clause if c != v]
                if len(new_clause) == 1:
                    unit_clauses.add(new_clause)
    return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        variables, clauses = tseitin_formula(n)
        G = {v: [] for v in variables}
        for clause in clauses:
            for v in clause:
                if v[0] == '-':
                    u = v[1:]
                    G[u].append(clause)
                else:
                    u = v
                    G[u].append([c for c in clauses if -v not in c])
        
        ν_G = len(G)  # Simplified symplectic form invariant for this example
        proof_length = resolution_length(G)
        
        results.append({
            "metric_name": "resolution_proof_length",
            "metric_value": proof_length,
            "instances_tested": 1,
            "conjecture_holds": proof_length >= 2**(math.log(ν_G, 2)),
            "counterexample": ""
        })
    
    mean = sum(result["metric_value"] for result in results) / len(results)
    std = math.sqrt(sum((result["metric_value"] - mean)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean": mean,
        "std": std,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean = sum(result["mean"] for result in results) / len(results)
    std = math.sqrt(sum((result["mean"] - mean)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["support_fraction"] >= 0.8) / len(results)
    
    if all(result["support_fraction"] >= 0.8 for result in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")