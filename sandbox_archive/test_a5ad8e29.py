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
    
    def generate_instance(n):
        A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        return A
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def characteristic_polynomial(A):
        n = len(A)
        p = [[0] * (n + 1) for _ in range(n)]
        p[0][0] = 1
        for i in range(1, n + 1):
            p[i % n] = matrix_multiplication(A, p[(i - 1) % n])
            p[i % n][-1] -= 1
        return p
    
    def min_p_adic_hodge_trace(poly):
        trace = 0
        for i in range(len(poly)):
            if poly[i][i] != 0:
                trace += abs(Fraction(poly[i][i]).limit_denominator())
        return trace
    
    def rank_variance(matrix):
        n = len(matrix)
        rank = 0
        A = [row[:] for row in matrix]
        for i in range(n):
            if A[i][i] != 0:
                pivot = Fraction(A[i][i]).limit_denominator()
                for j in range(i + 1, n):
                    factor = -Fraction(A[j][i], pivot).limit_denominator()
                    for k in range(n):
                        A[j][k] += factor * A[i][k]
            else:
                found_pivot = False
                for j in range(i + 1, n):
                    if A[j][i] != 0:
                        A[i][:], A[j][:] = A[j][:], A[i][:]
                        found_pivot = True
                        break
                if not found_pivot:
                    continue
            rank += 1
        return (n - rank) ** 2
    
    def run_instance(n):
        A = generate_instance(n)
        poly = characteristic_polynomial(A)
        trace = min_p_adic_hodge_trace(poly)
        variance = rank_variance(A)
        return trace, variance
    
    n_values = [5, 10, 15, 20, 30, 40]
    traces = []
    variances = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            trace, variance = run_instance(n)
            traces.append(trace)
            variances.append(variance)
    
    correlation_coefficient = sum(t * v for t, v in zip(traces, variances)) / (sum(traces) ** 2 + sum(variances) ** 2)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(traces),
        "n_max": max(n_values),
        "conjecture_holds": 0.8 <= correlation_coefficient <= 1.2,
        "counterexample": "" if 0.8 <= correlation_coefficient <= 1.2 else "Correlation out of bounds"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 999997) for _ in range(30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation out of bounds\" first_failing_seed={first_failing_seed}")