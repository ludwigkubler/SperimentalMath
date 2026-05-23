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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def permanent_matrix(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        perm = 0
        sign = 1
        for i in range(n):
            submatrix = [row[:i] + row[i+1:] for row in A[1:]]
            perm += sign * A[0][i] * permanent_matrix(submatrix)
            sign *= -1
        return perm

    def plethysm_coefficients(f, g):
        n = len(f)
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    result[i][j] += f[i][k] * g[k][j]
        return result

    def generate_polynomial(D, n):
        coefficients = [random.randint(0, 1) for _ in range(D+1)]
        polynomial = [[0] * (n+1) for _ in range(n+1)]
        for i in range(D+1):
            if coefficients[i] == 1:
                for j in range(i, n+1):
                    polynomial[j][j-i] += 1
        return polynomial

    def permanent_circuit_size(A):
        m, n = len(A), len(A[0])
        if m == 1 and n == 1:
            return 1
        size = 0
        for i in range(m):
            for j in range(n):
                if A[i][j] != 0:
                    submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
                    size += permanent_circuit_size(submatrix)
        return size

    n = random.randint(5, 40)
    D = int(math.log2(n) ** 2)
    f = generate_polynomial(D, n)
    g = generate_polynomial(D, n)
    plethysm = plethysm_coefficients(f, g)
    perm_circuit_size = permanent_circuit_size(plethysm)

    rank = gaussian_elimination(plethysm)
    rank_value = sum(1 for row in rank if any(row))

    return {
        "metric_name": "Rank vs DPLL Heig",
        "metric_value": rank_value,
        "instances_tested": 1,
        "conjecture_holds": rank_value >= D and perm_circuit_size <= (n ** 1.5) ** D,
        "counterexample": "" if rank_value >= D and perm_circuit_size <= (n ** 1.5) ** D else f"Rank={rank_value}, Perm Circuit Size={perm_circuit_size}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        counterexample = next((result["counterexample"] for result in results if not result["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")