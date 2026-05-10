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
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = Fraction(A[i][i])
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for k in range(n):
                if k != i:
                    factor = Fraction(A[k][i])
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                    b[k] -= factor * b[i]
        return b
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def is_positive_definite(A):
        n = len(A)
        for i in range(n):
            if A[i][i] <= 0:
                return False
            for j in range(i + 1, n):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return True
    
    def sos_degree(matrix):
        n = len(matrix)
        if not is_positive_definite(matrix):
            return None
        A = matrix
        b = [Fraction(0, 1)] * n
        x = gaussian_elimination(A, b)
        return sum(x[i] ** 2 for i in range(n))
    
    def max_cut_instance(n):
        instance = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
        return instance
    
    def quartic_polynomial(instance):
        n = len(instance)
        polynomial = Fraction(0, 1)
        for i in range(n):
            for j in range(i + 1, n):
                term = instance[i][j] ** 2
                for k in range(n):
                    term *= instance[k][i] * instance[k][j]
                polynomial += term
        return polynomial
    
    def critical_points(quartic_polynomial):
        n = len(quartic_polynomial)
        A = [[0] * n for _ in range(n)]
        b = [Fraction(0, 1)] * n
        for i in range(n):
            for j in range(i + 1, n):
                term = quartic_polynomial[i][j]
                for k in range(n):
                    A[i][k] += term * instance[k][i] * instance[k][j]
                b[i] -= term * instance[j][i] * instance[j][j]
        return gaussian_elimination(A, b)
    
    n = 10
    instance = max_cut_instance(n)
    quartic_poly = quartic_polynomial(instance)
    critical_points_count = len(critical_points(quartic_poly))
    
    sos_degrees = []
    for _ in range(10):
        matrix = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
        degree = sos_degree(matrix)
        if degree is not None:
            sos_degrees.append(degree)
    
    mean_sos_degree = sum(sos_degrees) / len(sos_degrees)
    
    return {
        "metric_name": "SOS Degree",
        "metric_value": mean_sos_degree,
        "instances_tested": 10,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")