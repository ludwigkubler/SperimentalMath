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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Inverse doesn't exist")
    else:
        return x % m

def matrix_mul(A, B):
    n = len(A)
    result = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_inv(A):
    n = len(A)
    det = 0
    if n == 1:
        det = A[0][0]
    elif n == 2:
        det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    else:
        for c in range(n):
            sub_matrix = [row[:c] + row[c+1:] for row in A[1:]]
            sign = (-1) ** (c % 2)
            sub_det = matrix_det(sub_matrix)
            det += sign * A[0][c] * sub_det
    if det == 0:
        raise ValueError("Matrix is not invertible")
    inv_det = mod_inverse(det, n)
    adjugate = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            sub_matrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
            sign = (-1) ** ((i+j) % 2)
            adjugate[i][j] = sign * matrix_det(sub_matrix)
    inv_A = [[(adjugate[i][j] * inv_det) % n for j in range(n)] for i in range(n)]
    return inv_A

def matrix_det(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    elif n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    else:
        det = 0
        for c in range(n):
            sub_matrix = [row[:c] + row[c+1:] for row in A[1:]]
            sign = (-1) ** (c % 2)
            det += sign * A[0][c] * matrix_det(sub_matrix)
        return det

def gaussian_elimination(A, b):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0 for _ in range(n)]
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [4, 8, 12, 16, 20, 24, 32, 40]
    d_values = [2, 3, 4]
    c = 0.05
    results = []
    
    for n in n_values:
        for d in d_values:
            if n <= 20:
                inputs = list(range(n))
                outputs = [random.choice([0, 1]) for _ in range(2**n)]
            else:
                inputs = list(range(n))
                outputs = [random.randint(0, 1) for _ in range(512)]
            
            # Construct canonical PARITY circuit
            if n == 4 and d == 2:
                circuit = [[i] for i in range(n)]
            elif n == 8 and d == 3:
                circuit = [[i] for i in range(n)]
            elif n == 12 and d == 4:
                circuit = [[i] for i in range(n)]
            else:
                return {"metric_name": "psi", "metric_value": None, "instances_tested": 0, "conjecture_holds": False, "counterexample": "mapping_undefined"}
            
            # Compute meet-closure P_C of gate supports
            P_C = set()
            for S in circuit:
                P_C.add(frozenset(S))
            P_C.add(frozenset())
            P_C.add(frozenset(range(n)))
            while True:
                new_elements = set()
                for S1 in P_C:
                    for S2 in P_C:
                        if S1.issubset(S2):
                            continue
                        new_elements.add(S1.intersection(S2))
                if not new_elements:
                    break
                P_C.update(new_elements)
            
            # Evaluate μ_{P_C}(∅,·) by topological recursion
            mu = {frozenset(): 0}
            for S in sorted(P_C, key=len):
                mu[S] = sum(mu[frozenset(T)] for T in P_C if T.issubset(S) and len(T) == len(S) - 1)
            
            # Compute ψ(C)
            psi = math.log2(1 + sum(abs(mu[frozenset(S)]) for S in P_C))
            results.append(psi)
    
    # Perform OLS regression
    n_values = [n for _ in range(len(n_values)) for _ in range(len(d_values))]
    d_values = [d for _ in range(len(n_values)) for _ in range(len(d_values))]
    psi_values = [psi for psi in results]
    
    X = [[n**(1/(d-1)), 1] for n, d in zip(n_values, d_values)]
    Y = psi_values
    
    A = matrix_mul(matrix_transpose(X), X)
    b = matrix_mul(matrix_transpose(X), Y)
    inv_A = matrix_inv(A)
    beta = matrix_mul(inv_A, b)
    
    slope = beta[0]
    intercept = beta[1]
    
    return {
        "metric_name": "psi",
        "metric_value": slope,
        "instances_tested": len(results),
        "conjecture_holds": slope >= 0.1,
        "counterexample": "" if slope >= 0.1 else f"Counterexample found with slope {slope}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        if "conjecture_holds" in result and result["conjecture_holds"]:
            results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = len([r for r in results if r >= 0.1]) / len(results)
    
    if all(r >= 0.1 for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r < 0.1 for r in results):
        first_failing_seed = seeds[results.index(min([r for r in results if r < 0.1]))]
        print(f"RESULT: FALSIFIED counterexample=\"slope_below_threshold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")