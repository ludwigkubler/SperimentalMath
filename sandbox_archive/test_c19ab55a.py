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
        max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1) ** j * A[0][j] * determinant(submatrix)
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    m = random.randint(5, 30)
    
    # Generate a random CNF formula with n variables and m clauses
    phi = []
    for _ in range(m):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        phi.append(clause)
    
    # Define the Hodge Laplacian matrix for the quaternionic Kähler metrics
    H = [[0] * n for _ in range(n)]
    for clause in phi:
        for x in clause:
            for y in clause:
                if x != y:
                    i, j = abs(x) - 1, abs(y) - 1
                    H[i][j] += 1
    
    # Compute the eigenvalues of the Hodge Laplacian matrix
    eigenvalues = []
    A = H.copy()
    while len(A) > 0:
        A = gaussian_elimination(A)
        det_A = determinant(A)
        if det_A != 0:
            eigenvalues.append(det_A)
        A.pop(0)
    
    # Compute the maximum eigenvalue
    max_eigenvalue = max(eigenvalues)
    
    # Define the function f(n, m) = Θ(m^(3/2)n^(1/4))
    f_nm = math.sqrt(m) * n ** 0.25
    
    # Check if the conjecture holds
    conjecture_holds = max_eigenvalue <= f_nm
    
    return {
        "metric_name": "max_eigenvalue",
        "metric_value": max_eigenvalue,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"phi={phi}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")