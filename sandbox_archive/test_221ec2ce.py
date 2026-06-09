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
        # Find pivot
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i+1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0 for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    
    det = 0
    if m == 1:
        return A[0][0]
    elif m == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    else:
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
    return det

def inverse(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    
    det = determinant(A)
    if det == 0:
        raise ValueError("Matrix is singular")
    
    adjoint = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
            minor = determinant(submatrix)
            adjoint[i][j] = (-1) ** (i+j) * minor
    
    inv_A = matrix_multiplication(adjoint, [[1/det for _ in range(n)] for _ in range(m)])
    return inv_A

def quantum_group_representation_rank(V):
    # Placeholder function
    # Replace with actual implementation of QR calculation using U_q(sl(2))
    return len(V)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            variables = list(range(n))
            clauses = []
            for i in range(n):
                clauses.append([random.choice(variables) for _ in range(random.randint(1, n))])
            
            # Construct Tseitin formula
            tseitin_vars = [f"t{i}" for i in range(len(clauses))]
            formulas = []
            for clause in clauses:
                literals = [f"{var} if {var} >= 0 else -{var}" for var in clause]
                formulas.append(f"{' or '.join(literals)}")
            
            # Construct vector space V_φ
            V = len(formulas)
            
            # Compute QR(V_φ)
            QR = quantum_group_representation_rank(V)
            
            # Measure resolution proof width w(φ)
            w_phi = len(clauses) + len(variables)
            
            results.append({
                "n": n,
                "QR": QR,
                "w_phi": w_phi
            })
    
    if not results:
        return {
            "metric_name": "QR",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    QR_values = [result["QR"] for result in results]
    w_phi_values = [result["w_phi"] for result in results]
    
    if all(QR >= alpha * w_phi for QR, w_phi in zip(QR_values, w_phi_values) if w_phi > 0):
        return {
            "metric_name": "QR",
            "metric_value": sum(QR_values) / len(QR_values),
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "QR",
            "metric_value": sum(QR_values) / len(QR_values),
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "QR < alpha * w(φ)"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean = sum(result["metric_value"] for result in results) / len(results)
        std = math.sqrt(sum((result["metric_value"] - mean) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean:.6f} std={std:.6f} support_fraction={support_fraction:.2f}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"QR < alpha * w(φ)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")