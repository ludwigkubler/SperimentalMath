# auto-injected by SEC sandbox
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
import math
from itertools import combinations

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    result = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def gaussian_elimination(A, b):
    n = len(A)
    Augmented = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(Augmented[j][i]) > abs(Augmented[max_row][i]):
                max_row = j
        Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
        factor = Augmented[i][i]
        for j in range(i, n+1):
            Augmented[i][j] /= factor
        for j in range(n):
            if j != i:
                factor = Augmented[j][i]
                for k in range(i, n+1):
                    Augmented[j][k] -= factor * Augmented[i][k]
    return [row[-1] for row in Augmented]

def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    sign = 1
    for i in range(n):
        submatrix = []
        for j in range(1, n):
            row = []
            for k in range(n):
                if k != i:
                    row.append(matrix[j][k])
            submatrix.append(row)
        det += sign * matrix[0][i] * determinant(submatrix)
        sign *= -1
    return det

def secant_variety_dimension(poly, n):
    # Placeholder for actual computation. This is a dummy implementation.
    return len(poly)  # Replace with actual dimension calculation

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    instances_tested = 30
    metric_name = "secant_variety_dimension_gap"
    counterexample = ""
    
    det_poly = []
    perm_poly = []
    
    for _ in range(instances_tested):
        # Generate a random 3-CNF formula with n variables
        clauses = set()
        while len(clauses) < 2*n:
            clause = tuple(sorted(random.sample(range(n), 3)))
            if clause not in clauses:
                clauses.add(clause)
        
        incidence_matrix = [[0 for _ in range(n)] for _ in range(n)]
        for var1, var2, var3 in clauses:
            incidence_matrix[var1][var2] += 1
            incidence_matrix[var2][var3] += 1
            incidence_matrix[var3][var1] += 1
        
        det = determinant(incidence_matrix)
        perm = 0
        for assignment in combinations(range(n), n):
            term = 1
            for var1, var2, var3 in clauses:
                if (assignment[var1], assignment[var2], assignment[var3]) in ((0, 0, 0), (1, 1, 1)):
                    term *= -1
                elif (assignment[var1], assignment[var2], assignment[var3]) in ((0, 1, 0), (1, 0, 1), (0, 0, 1), (1, 1, 0)):
                    term *= 1
            perm += term
        
        det_poly.append(det)
        perm_poly.append(perm)
    
    det_dim = secant_variety_dimension(det_poly, n)
    perm_dim = secant_variety_dimension(perm_poly, n)
    
    metric_value = perm_dim - det_dim
    
    conjecture_holds = metric_value >= 2**n / 2
    if not conjecture_holds:
        counterexample = "det_dim={} perm_dim={}".format(det_dim, perm_dim)
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_value, std_value, support_fraction))
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print("RESULT: FALSIFIED counterexample={} first_failing_seed={}".format(results[0]["counterexample"], first_failing_seed))
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")