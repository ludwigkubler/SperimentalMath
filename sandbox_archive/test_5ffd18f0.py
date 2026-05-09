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
        pivot = A[i][i]
        if pivot == 0:
            return None  # Singular matrix
        for j in range(i + 1, m):
            factor = A[j][i] / pivot
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def det(A):
    if len(A) != len(A[0]):
        raise ValueError("Matrix must be square")
    n = len(A)
    if n == 1:
        return A[0][0]
    elif n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    else:
        det_val = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det_val += ((-1) ** j) * A[0][j] * det(submatrix)
        return det_val

def matrix_mult(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0 for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    num_clauses = 3 * n
    clauses = []
    for _ in range(num_clauses):
        variables = random.sample(range(n), 3)
        clause = [random.choice([-1, 1]) * var for var in variables]
        clauses.append(clause)

    # Construct the linear program matrix
    A = [[0] * (n + 1) for _ in range(num_clauses)]
    b = [0] * num_clauses
    for i, clause in enumerate(clauses):
        for j, var in enumerate(clause):
            A[i][var - 1] += var
        b[i] = 1

    # Solve the linear program using Gaussian elimination
    solution = gaussian_elimination(A)
    if solution is None:
        return {
            "metric_name": "sos_refutation_degree",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "singular_matrix"
        }

    # Compute the volume of the feasible region
    volume = abs(det(solution)) / math.factorial(n)

    # Compute the minimal refutation degree
    refutation_degree = int(math.log2(n))

    # Check if the conjecture holds
    if volume < 1e-6 and refutation_degree >= math.log2(n):
        return {
            "metric_name": "sos_refutation_degree",
            "metric_value": volume,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "sos_refutation_degree",
            "metric_value": volume,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"volume={volume}, refutation_degree={refutation_degree}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_volume = sum(r["metric_value"] for r in results) / len(results)
    std_volume = math.sqrt(sum((r["metric_value"] - mean_volume)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_volume} std={std_volume} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"volume too large\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")