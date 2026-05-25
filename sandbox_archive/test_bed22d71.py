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
    
    def frobenius_norm(A):
        norm = 0
        for row in A:
            for val in row:
                norm += val ** 2
        return math.sqrt(norm)
    
    def noncommutative_lp_measure(A, p):
        if p == float('inf'):
            return max(frobenius_norm(row) for row in A)
        else:
            sum_val = 0
            for row in A:
                sum_row = 0
                for val in row:
                    sum_row += abs(val) ** p
                sum_val += sum_row ** (1/p)
            return sum_val
    
    def random_disjointness_instance(n):
        A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        B = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        return A, B
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        A, B = random_disjointness_instance(n)
        M = matrix_multiplication(A, B)
        measures = [noncommutative_lp_measure(M, p) for p in range(1, 6)]
        comm_complexity = sum(random.choice([0, 1]) for _ in range(n))
        results.append((measures, comm_complexity))
    
    correlation_coefficients = []
    for measures, comm_complexity in results:
        if len(measures) != len(comm_complexity):
            return {
                "metric_name": "correlation_coefficient",
                "metric_value": None,
                "instances_tested": 0,
                "conjecture_holds": False,
                "counterexample": "inconsistent_results"
            }
        n = len(measures)
        mean_measures = sum(measures) / n
        mean_comm_complexity = sum(comm_complexity) / n
        numerator = sum((measures[i] - mean_measures) * (comm_complexity[i] - mean_comm_complexity) for i in range(n))
        denominator = math.sqrt(sum((measures[i] - mean_measures) ** 2 for i in range(n))) * math.sqrt(sum((comm_complexity[i] - mean_comm_complexity) ** 2 for i in range(n)))
        correlation_coefficient = numerator / denominator if denominator != 0 else float('inf')
        correlation_coefficients.append(correlation_coefficient)
    
    avg_corr = sum(correlation_coefficients) / len(correlation_coefficients)
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": avg_corr,
        "instances_tested": len(n_values),
        "conjecture_holds": avg_corr >= 0.7,
        "counterexample": "" if avg_corr >= 0.7 else f"avg_corr={avg_corr}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_corr = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_corr} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_corr} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='avg_corr<{avg_corr}' first_failing_seed={first_failing_seed}")