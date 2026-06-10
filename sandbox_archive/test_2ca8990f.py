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
        n = len(A)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor
            for j in range(n):
                if i != j:
                    factor = Fraction(A[j][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def rank(matrix):
        matrix_copy = [row[:] for row in matrix]
        gaussian_elimination(matrix_copy)
        rank = 0
        for row in matrix_copy:
            if any(row):
                rank += 1
        return rank

    def communication_complexity_instance(n, m):
        A = [[random.randint(0, 1) for _ in range(m)] for _ in range(n)]
        B = [[random.randint(0, 1) for _ in range(m)] for _ in range(n)]
        return A, B

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        phi_A, phi_B = communication_complexity_instance(n, n)
        min_order_KM = rank(matrix_multiplication(phi_A, phi_B))
        O_phi = sum(sum(row) for row in phi_A) + sum(sum(row) for row in phi_B)
        results.append({
            "n": n,
            "min_order_KM": min_order_KM,
            "O_phi": O_phi
        })
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    min_order_KM_values = [r["min_order_KM"] for r in results]
    O_phi_values = [r["O_phi"] for r in results]
    
    mean_min_order_KM = sum(min_order_KM_values) / len(min_order_KM_values)
    mean_O_phi = sum(O_phi_values) / len(O_phi_values)
    
    correlation_coefficient = 0
    if mean_min_order_KM != 0 and mean_O_phi != 0:
        numerator = sum((min_order_KM_values[i] - mean_min_order_KM) * (O_phi_values[i] - mean_O_phi) for i in range(len(min_order_KM_values)))
        denominator = math.sqrt(sum((min_order_KM_values[i] - mean_min_order_KM) ** 2 for i in range(len(min_order_KM_values)))) * math.sqrt(sum((O_phi_values[i] - mean_O_phi) ** 2 for i in range(len(O_phi_values))))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(min_order_KM_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None)) / len([r for r in results if r["metric_value"] is not None])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "first_failing_seed" if first_failing_seed is not None else ""
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")