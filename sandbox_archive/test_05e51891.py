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
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        factor = 1 / A[i][i]
        for j in range(n):
            A[i][j] *= factor
        for j in range(n):
            if i != j:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    sign = 1
    for i in range(n):
        submatrix = [row[:i] + row[i+1:] for row in A[1:]]
        det += sign * A[0][i] * determinant(submatrix)
        sign *= -1
    return det

def eigenvalues(A):
    n = len(A)
    if n == 2:
        a, b, c, d = A[0][0], A[0][1], A[1][0], A[1][1]
        return [(a + d) / 2 + math.sqrt((a + d)**2 - 4 * (a*d - b*c)) / 2,
                (a + d) / 2 - math.sqrt((a + d)**2 - 4 * (a*d - b*c)) / 2]
    else:
        det = determinant(A)
        if det == 0:
            return [0] * n
        eigenvals = []
        for i in range(n):
            submatrix = [row[:i] + row[i+1:] for row in A[1:]]
            eigenvals.append(-A[0][i] / determinant(submatrix))
        return eigenvals

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    R_f = [sum(row[i] for row in f) % 2 for i in range(n)]
    
    # Construct the matrix representation of f
    A = []
    for i in range(n):
        row = [f[j][i] for j in range(n)]
        A.append(row)
    
    gaussian_elimination(A)
    rank_A = sum(1 for row in A if any(val != 0 for val in row))
    
    # Compute the eigenvalues of A
    eigs = eigenvalues(A)
    min_non_zero_eig = min(eig for eig in eigs if eig != 0)
    
    return {
        "metric_name": "minrank(BrauerGroup(V(f))) / max_k |λ_k(f)|",
        "metric_value": rank_A / abs(min_non_zero_eig),
        "instances_tested": 1,
        "conjecture_holds": rank_A <= abs(min_non_zero_eig),
        "counterexample": "" if rank_A <= abs(min_non_zero_eig) else "minrank(BrauerGroup(V(f))) > max_k |λ_k(f)|"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*37, 4))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(res["metric_value"] for res in results) / len(results)
    std_metric = math.sqrt(sum((res["metric_value"] - mean_metric)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"minrank(BrauerGroup(V(f))) > max_k |λ_k(f)|\" first_failing_seed={first_failing_seed}")