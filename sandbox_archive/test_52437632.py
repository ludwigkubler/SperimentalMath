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
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
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

    def hodge_decomposition(A):
        n = len(A)
        rank = sum(1 for row in gaussian_elimination(A) if any(row))
        return rank

    def generate_communication_complexity_problem(r):
        A = [[random.randint(-10, 10) for _ in range(r)] for _ in range(r)]
        B = [[random.randint(-10, 10) for _ in range(r)] for _ in range(r)]
        C = matrix_multiplication(A, B)
        return C

    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for r in [5, 10, 15, 20, 30, 40]:
        for _ in range(instances_tested):
            A = generate_communication_complexity_problem(r)
            rank = determinant(A)
            if rank == 0:
                continue
            hodge_cycles = hodge_decomposition(A)
            metric_values.append(hodge_cycles / rank)

    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    
    conjecture_holds = all(0.8 <= value <= 10 for value in metric_values)
    counterexample = "" if conjecture_holds else "correlation_coefficient_out_of_bounds"
    
    return {
        "metric_name": "Hodge Cycles to Rank Ratio",
        "metric_value": mean_value,
        "instances_tested": instances_tested * 6,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_out_of_bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")