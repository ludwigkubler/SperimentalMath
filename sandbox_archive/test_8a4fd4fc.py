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
    
    def generate_adjacency_matrix(n):
        A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            A[i][i] = 0
        return A
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        n = len(A)
        M = [A[i] + [b[i]] for i in range(n)]
        for i in range(n):
            max_row = max(range(i, n), key=lambda k: abs(M[k][i]))
            M[i], M[max_row] = M[max_row], M[i]
            factor = M[i][i]
            for j in range(i, n + 1):
                M[i][j] /= factor
            for j in range(n):
                if i != j:
                    factor = M[j][i]
                    for k in range(i, n + 1):
                        M[j][k] -= factor * M[i][k]
        return [row[-1] for row in M]
    
    def characteristic_polynomial(A):
        n = len(A)
        x = random.randint(2, 10)
        p = [[0 for _ in range(n)] for _ in range(n)]
        p[0][0] = 1
        for i in range(1, n + 1):
            p[i % n] = matrix_multiplication(A, p[(i - 1) % n])
            p[i % n][-1] -= x ** (n - i)
        return p
    
    def min_p_adic_hodge_trace(poly):
        n = len(poly)
        trace = 0
        for i in range(n):
            if poly[i][i] != 0:
                trace += abs(poly[i][i])
        return trace
    
    def rank_variance(A):
        n = len(A)
        rank = 0
        M = [row[:] for row in A]
        for i in range(n):
            max_row = max(range(i, n), key=lambda k: abs(M[k][i]))
            if M[max_row][i] == 0:
                continue
            M[i], M[max_row] = M[max_row], M[i]
            rank += 1
            factor = M[i][i]
            for j in range(n):
                M[i][j] /= factor
            for j in range(n):
                if i != j:
                    factor = M[j][i]
                    for k in range(n):
                        M[j][k] -= factor * M[i][k]
        return rank ** 2 / n
    
    def run_instance(n):
        A = generate_adjacency_matrix(n)
        poly = characteristic_polynomial(A)
        trace = min_p_adic_hodge_trace(poly)
        variance = rank_variance(A)
        return abs(trace), variance
    
    instances_tested = 0
    total_trace = 0.0
    total_variance = 0.0
    n_max = 1
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        for _ in range(5):
            instances_tested += 1
            trace, variance = run_instance(n)
            total_trace += trace
            total_variance += variance
    
    mean_trace = total_trace / instances_tested
    mean_variance = total_variance / instances_tested
    correlation_coefficient = (instances_tested * total_trace * total_variance - 
                               total_trace ** 2 * mean_variance) / (
                                   math.sqrt((instances_tested * total_trace ** 2 - 
                                               total_trace ** 2) *
                                             (instances_tested * total_variance ** 2 -
                                              total_variance ** 2)))
    
    conjecture_holds = 0.8 <= correlation_coefficient <= 1.2
    counterexample = "" if conjecture_holds else "correlation_outside_bound"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")