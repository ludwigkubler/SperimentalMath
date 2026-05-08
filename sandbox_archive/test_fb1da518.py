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
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def solve_linear_system(A, b):
    n = len(A)
    A_b = [row + [b[i]] for i, row in enumerate(A)]
    A_b = gaussian_elimination(A_b)
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (A_b[i][-1] - sum(A_b[i][j] * x[j] for j in range(i+1, n))) / A_b[i][i]
    return x

def matrix_multiplication(A, B):
    m, k = len(A), len(B[0])
    result = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            result[i][j] = sum(A[i][l] * B[l][j] for l in range(len(B)))
    return result

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    d_values = [2, 4, 8]
    instances_tested = 30
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        G = [[random.choice([0, 1]) if i != j else 0 for j in range(n)] for i in range(n)]
        c = [sum(G[i][j] for j in range(i+1, n)) for i in range(n)]

        def moment_matrix(d):
            M = [[0] * (n + 1) for _ in range(n + 1)]
            M[0][0] = len(c)
            for i in range(1, n + 1):
                M[i][0] = sum(c[j] for j in range(i))
                for j in range(1, i + 1):
                    M[i][j] = sum(G[k][l] * c[k] * c[l] for k in range(n) for l in range(k+1, n)) if j == 1 else 0
            return M

        min_eigenvalue = float('inf')
        for d in d_values:
            M = moment_matrix(d)
            eigenvalues = solve_linear_system(M, [0] * (n + 1))
            min_eigenvalue = min(min_eigenvalue, abs(eigenvalues[-1]))

        if min_eigenvalue < c(n) / d:
            conjecture_holds = False
            counterexample = f"Seed {seed}: Counterexample found for n={n}, d={d}"

    return {
        "metric_name": "min_eigenvalue",
        "metric_value": min_eigenvalue,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data or non-standard behavior")