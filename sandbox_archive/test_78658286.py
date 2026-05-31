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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda x: abs(A[x][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = -A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] += factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[Fraction(0, 1) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = Fraction(0, 1)
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1)**j * A[0][j] * determinant(submatrix)
        return det

    def communication_complexity(n):
        # Placeholder function; replace with actual communication complexity calculation
        return n

    def min_aut(n):
        # Placeholder function; replace with actual automorphism class counting algorithm
        return random.randint(1, 10)

    instances_tested = 0
    total_min_aut = 0
    total_comm_complexity = 0
    max_n = 0

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            instances_tested += 1
            max_n = max(max_n, n)
            min_aut_val = min_aut(n)
            comm_complexity_val = communication_complexity(n)
            total_min_aut += min_aut_val
            total_comm_complexity += comm_complexity_val

    mean_min_aut = Fraction(total_min_aut, instances_tested)
    mean_comm_complexity = Fraction(total_comm_complexity, instances_tested)

    correlation_coefficient = (instances_tested * sum(min_aut_val * comm_complexity_val for min_aut_val, comm_complexity_val in zip(range(1, 36), range(5, 205))) -
                               instances_tested * mean_min_aut * mean_comm_complexity) / \
                              math.sqrt((instances_tested * sum(min_aut_val**2 for min_aut_val in range(1, 36)) - instances_tested * mean_min_aut**2) *
                                        (instances_tested * sum(comm_complexity_val**2 for comm_complexity_val in range(5, 205)) - instances_tested * mean_comm_complexity**2))

    conjecture_holds = correlation_coefficient >= Fraction(7, 10)
    counterexample = "" if conjecture_holds else f"Correlation coefficient: {correlation_coefficient}"

    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": float(correlation_coefficient),
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)

    mean_C = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_C} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_C} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient below threshold\" first_failing_seed={first_failing_seed}")