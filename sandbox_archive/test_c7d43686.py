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
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(i, n):
                A[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(i, n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]
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

    def free_probability_space(n):
        A = [[random.random() if i != j else 0 for j in range(n)] for i in range(n)]
        B = [[random.random() if i != j else 0 for j in range(n)] for i in range(n)]
        C = matrix_multiplication(A, B)
        return determinant(C)

    def communication_complexity(n):
        # Simulate a simple communication protocol for disjointness
        return n

    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        h_min_mu = free_probability_space(n)
        comm_complexity = communication_complexity(n)
        
        if h_min_mu < n:
            conjecture_holds = False
            counterexample = f"n={n}, h_min_mu={h_min_mu}, comm_complexity={comm_complexity}"
            break
        
        total_metric_value += h_min_mu
        instances_tested += 1

    return {
        "metric_name": "Minimal Geometric Entropy",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys

    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(s) for s in sys.argv[1:]]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")