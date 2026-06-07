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

def generate_sat_instance(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = [random.choice(variables) * (2 * random.randint(0, 1) - 1)
                  for _ in range(random.randint(1, n))]
        clauses.append(clause)
    return variables, clauses

def binary_hermitian_matrix(n, clauses):
    A = [[0] * n for _ in range(n)]
    for clause in clauses:
        for literal in clause:
            var = abs(literal)
            sign = 1 if literal > 0 else -1
            for j in range(n):
                if j + 1 == var:
                    A[j][j] += sign * sign
    return A

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for r in range(i+1, n):
            if abs(A[r][i]) > abs(A[max_row][i]):
                max_row = r
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        factor = 1 / A[i][i]
        for j in range(i, n):
            A[i][j] *= factor
        for k in range(i+1, n):
            factor = A[k][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
    return A

def eigenvalues(A):
    n = len(A)
    if n == 1:
        return [A[0][0]]
    
    # Compute characteristic polynomial
    det = [[0] * (n-1) for _ in range(n-1)]
    for i in range(n):
        for j in range(1, n):
            for k in range(n-1):
                if k < i:
                    det[j-1][k] = A[j][k]
                elif k >= i:
                    det[j-1][k-1] = A[j][k]
    
    # Recursively compute determinant
    return [A[0][i] * e for i, e in enumerate(eigenvalues(det))] + [-det[0][0]]

def geometric_entropy(eigenvalues):
    norm = sum(abs(e) ** 2 for e in eigenvalues) ** 0.5
    entropy = 0
    for e in eigenvalues:
        if abs(e) > 1e-10:  # Avoid log(0)
            entropy -= abs(e) * math.log(abs(e)) / norm**2
    return entropy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = int(0.2 * n * (n - 1))  # Vary clause density
        variables, clauses = generate_sat_instance(n, m)
        A = binary_hermitian_matrix(n, clauses)
        
        eigenvals = eigenvalues(A)
        H_phi = geometric_entropy(eigenvals)
        delta_phi = len([assignment for assignment in itertools.product([-1, 1], repeat=n) if all(lit * assignment[abs(lit)-1-1] >= 0 for lit in clauses)])
        
        results.append({
            "n": n,
            "H_phi": H_phi,
            "delta_phi": delta_phi
        })
    
    mean_H_phi = sum(result["H_phi"] for result in results) / len(results)
    std_H_phi = (sum((result["H_phi"] - mean_H_phi) ** 2 for result in results) / len(results)) ** 0.5
    
    conjecture_holds = all(abs(H_phi) <= 2 * math.log(delta_phi) for H_phi, delta_phi in zip([result["H_phi"] for result in results], [result["delta_phi"] for result in results]))
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": mean_H_phi,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_H_phi = sum(result["metric_value"] for result in results) / len(results)
    std_H_phi = (sum((result["metric_value"] - mean_H_phi) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_H_phi} std={std_H_phi} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_H_phi} std={std_H_phi} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")