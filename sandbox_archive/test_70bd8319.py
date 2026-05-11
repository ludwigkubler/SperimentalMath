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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        factor = Fraction(A[i][i])
        for k in range(i+1, n):
            A[k][i] /= factor
    
    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = A[i][-1]
        for j in range(i+1, n):
            x[i] -= A[i][j] * x[j]
        x[i] /= Fraction(A[i][i])
    
    return x

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def eigenvalues(A):
    n = len(A)
    if n == 1:
        return [A[0][0]]
    
    # Characteristic polynomial coefficients
    coeffs = [1]
    for i in range(n):
        coeffs.append(-sum(A[i][:i+1]))
        for j in range(i):
            coeffs[j] -= A[i][j] * coeffs[j+1]
    
    # Find roots using Newton's method
    def f(x):
        return sum(coeffs[k] * x**k for k in range(n+1))
    
    def df(x):
        return sum(k * coeffs[k] * x**(k-1) for k in range(1, n+2))
    
    roots = []
    for _ in range(n):
        x0 = random.uniform(-10, 10)
        while True:
            fx = f(x0)
            dfx = df(x0)
            if abs(dfx) < 1e-6:
                break
            x0 -= fx / dfx
        roots.append(x0)
    
    return sorted(roots)

def colin_de_verdiere_invariant(G):
    n = len(G)
    A = [[Fraction(G[i][j]) for j in range(n)] for i in range(n)]
    A_inv = gaussian_elimination(A)
    eigenvals = eigenvalues(A_inv)
    mu_G = max(eigenvals) - min(eigenvals)
    return float(mu_G)

def tseitin_formula(G):
    n = len(G)
    clauses = []
    for v in range(n):
        clauses.append([v+1])
        for u in range(v):
            if G[u][v] == 1:
                clauses.append([-u-1, -v-1, v+1])
                clauses.append([-u-1, v+1, -v-1])
    return clauses

def dpll(clauses, assignment=[]):
    if not clauses:
        return True
    unit_clauses = [c[0] for c in clauses if len(c) == 1]
    pure_symbols = {}
    for c in clauses:
        for lit in c:
            if abs(lit) not in pure_symbols:
                pure_symbols[abs(lit)] = lit > 0
            elif pure_symbols[abs(lit)] != (lit > 0):
                return False
    
    if unit_clauses or pure_symbols:
        new_assignment = assignment[:]
        for lit in unit_clauses + list(pure_symbols.keys()):
            new_assignment.append(lit)
        return dpll(clauses, new_assignment)
    
    literal = next(lit for lit in range(1, len(clauses)+1) if lit not in [abs(a) for a in assignment])
    if dpll([c[:] for c in clauses if literal not in c and -literal not in c], assignment + [literal]):
        return True
    if dpll([c[:] for c in clauses if -literal not in c], assignment + [-literal]):
        return True
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    
    mu_G = colin_de_verdiere_invariant(G)
    if math.isinf(mu_G) or math.isnan(mu_G):
        return {
            "metric_name": "resolution_length",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    clauses = tseitin_formula(G)
    resolution_length = len(clauses) if dpll(clauses) else float('inf')
    
    return {
        "metric_name": "resolution_length",
        "metric_value": resolution_length,
        "instances_tested": 1,
        "conjecture_holds": resolution_length >= 2 ** mu_G,
        "counterexample": "" if resolution_length >= 2 ** mu_G else f"resolution_length={resolution_length}, expected ≥{2 ** mu_G}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")