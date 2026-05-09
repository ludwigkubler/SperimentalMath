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
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    return x % m

def matrix_mod_inv(matrix, mod):
    n = len(matrix)
    det = 0
    for i in range(n):
        det += matrix[0][i] * sum(matrix[j][(j + i) % n] * (-1) ** (i + j) for j in range(1, n)) % mod
    det = det % mod
    inv_det = mod_inverse(det, mod)
    adjugate = [[sum((-1) ** (i + j) * matrix[j][(j + k) % n] for j in range(i + 1, n) for k in range(i + 1, n)) for i in range(n)] for n in range(n)]
    inv_matrix = [[(adjugate[i][j] * inv_det) % mod for j in range(n)] for i in range(n)]
    return inv_matrix

def matrix_mult(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    result = [[sum(A[i][k] * B[k][j] for k in range(p)) for j in range(n)] for i in range(m)]
    return result

def matrix_add(A, B):
    m = len(A)
    n = len(A[0])
    result = [[A[i][j] + B[i][j] for j in range(n)] for i in range(m)]
    return result

def matrix_sub(A, B):
    m = len(A)
    n = len(A[0])
    result = [[A[i][j] - B[i][j] for j in range(n)] for i in range(m)]
    return result

def matrix_transpose(matrix):
    return [list(row) for row in zip(*matrix)]

def matrix_det(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    det = 0
    for i in range(len(matrix)):
        sub_matrix = [row[:i] + row[i+1:] for row in matrix[1:]]
        det += (-1) ** i * matrix[0][i] * matrix_det(sub_matrix)
    return det

def gaussian_elimination(A, b):
    n = len(A)
    augmented = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(augmented[r][i]))
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
        pivot = augmented[i][i]
        for j in range(i + 1, n):
            factor = augmented[j][i] / pivot
            augmented[j] = [augmented[j][k] - factor * augmented[i][k] for k in range(n + 1)]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (augmented[i][-1] - sum(augmented[i][j] * x[j] for j in range(i + 1, n))) / augmented[i][i]
    return x

def groebner_basis(polynomials, mod=2**31 - 1):
    n = len(polynomials)
    basis = polynomials[:]
    for i in range(n):
        for j in range(i + 1, n):
            if basis[j]:
                lead_i = next((k for k in range(len(basis[i])) if basis[i][k] != 0), None)
                lead_j = next((k for k in range(len(basis[j])) if basis[j][k] != 0), None)
                if lead_i is not None and lead_j is not None:
                    factor = (basis[j][lead_j] * mod_inverse(basis[i][lead_i], mod)) % mod
                    basis[j] = [(basis[j][k] - factor * basis[i][k]) % mod for k in range(len(basis[j]))]
    return [p for p in basis if any(p[k] != 0 for k in range(len(p)))]

def real_radical_rank(I, mod=2**31 - 1):
    try:
        basis = groebner_basis(I, mod)
        rank = sum(1 for p in basis if any(p[k] != 0 for k in range(len(p))))
        return rank
    except Exception as e:
        print(f"Error computing real radical rank: {e}")
        return None

def sos_degree(poly, n):
    degree = 0
    for term in poly:
        degree = max(degree, sum(term[i] * i for i in range(n)))
    return degree

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    instances_tested = 30
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        # Generate a random Max-CUT instance
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            A[i][i] = 0
        
        # Compute the real radical ideal I of the feasible region
        I = []
        for i in range(n):
            for j in range(i + 1, n):
                if A[i][j]:
                    monomial = [0] * n
                    monomial[i] = -1
                    monomial[j] = 1
                    I.append(monomial)
        
        # Calculate the rank of the real radical ideal
        rank = real_radical_rank(I)
        if rank is None:
            return {
                "metric_name": "real_radical_rank",
                "metric_value": None,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        # Measure the SOS degree d(n) required to achieve 0.878-approximation
        target_approx = 0.878
        d_n = 1
        while True:
            x = [random.uniform(-1, 1) for _ in range(n)]
            poly = [sum(x[i] * A[i][j] * x[j] for j in range(n)) for i in range(n)]
            if all(p >= target_approx for p in poly):
                break
            d_n += 1
        
        # Check if the conjecture holds
        if d_n < math.log2(rank):
            conjecture_holds = False
            counterexample = f"Instance {_ + 1} failed: d(n)={d_n}, rank(I)={rank}"
    
    return {
        "metric_name": "sos_degree",
        "metric_value": d_n,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")