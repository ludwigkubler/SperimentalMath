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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def matrix_multiply(A, B):
        m = len(A)
        n = len(B[0])
        p = len(B)
        result = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    def matrix_add(A, B):
        return [[A[i][j] + B[i][j] for j in range(len(B[0]))] for i in range(len(A))]
    
    def matrix_sub(A, B):
        return [[A[i][j] - B[i][j] for j in range(len(B[0]))] for i in range(len(A))]
    
    def matrix_transpose(A):
        return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]
    
    def matrix_inverse(A):
        n = len(A)
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        for i in range(n):
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
                I[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                        I[k][j] -= factor * I[i][j]
        return I
    
    def matrix_determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * matrix_determinant(submatrix)
        return det
    
    def gaussian_elimination(A, b):
        n = len(A)
        for i in range(n):
            max_row = i
            for k in range(i+1, n):
                if abs(A[k][i]) > abs(A[max_row][i]):
                    max_row = k
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = A[i][i]
            for j in range(i, n):
                A[i][j] /= factor
            b[i] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(i, n):
                        A[k][j] -= factor * A[i][j]
                    b[k] -= factor * b[i]
        return [b[i] for i in range(n)]
    
    def compute_kostant_multiplicity(A):
        det_A = matrix_determinant(A)
        if det_A == 0:
            return None
        inv_A = matrix_inverse(A)
        trace_inv_A = sum(inv_A[i][i] for i in range(len(inv_A)))
        return abs(trace_inv_A) / det_A
    
    def compute_communication_complexity_rank_variance(f):
        n = len(f)
        rank = 0
        for i in range(2**n):
            row = [f[(i >> j) & 1] for j in range(n)]
            if any(row[j] != row[0] for j in range(1, n)):
                rank += 1
        return (rank - n) ** 2
    
    def run_instance(n):
        f = generate_boolean_function(n)
        A = [[f[(i >> j) & 1] * f[(j >> k) & 1] for k in range(n)] for j in range(n)]
        kappa = compute_kostant_multiplicity(A)
        if kappa is None:
            return None
        rank_variance = compute_communication_complexity_rank_variance(f)
        return kappa, rank_variance
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        instances_tested = 0
        kappa_sum = 0
        rank_variance_sum = 0
        for _ in range(5):
            instance_result = run_instance(n)
            if instance_result is not None:
                kappa, rank_variance = instance_result
                kappa_sum += kappa
                rank_variance_sum += rank_variance
                instances_tested += 1
        if instances_tested == 0:
            return {
                "metric_name": "Kostant Multiplicity vs Communication Complexity Rank Variance",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "No valid instances found"
            }
        kappa_avg = kappa_sum / instances_tested
        rank_variance_avg = rank_variance_sum / instances_tested
        results.append((kappa_avg, rank_variance_avg))
    
    if len(results) < 30:
        return {
            "metric_name": "Kostant Multiplicity vs Communication Complexity Rank Variance",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    kappa_values = [r[0] for r in results]
    rank_variance_values = [r[1] for r in results]
    mean_kappa = sum(kappa_values) / len(kappa_values)
    mean_rank_variance = sum(rank_variance_values) / len(rank_variance_values)
    correlation_sum = 0
    for kappa, rank_variance in zip(kappa_values, rank_variance_values):
        correlation_sum += (kappa - mean_kappa) * (rank_variance - mean_rank_variance)
    variance_kappa = sum((k - mean_kappa) ** 2 for k in kappa_values) / len(kappa_values)
    variance_rank_variance = sum((r - mean_rank_variance) ** 2 for r in rank_variance_values) / len(rank_variance_values)
    correlation_coefficient = correlation_sum / (math.sqrt(variance_kappa * variance_rank_variance))
    
    return {
        "metric_name": "Kostant Multiplicity vs Communication Complexity Rank Variance",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        if "conjecture_holds" in trial_result and not trial_result["conjecture_holds"]:
            print("RESULT: FALSIFIED counterexample=\"\" first_failing_seed={seed}")
            exit(0)
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")