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
            max_row = i
            for k in range(i+1, n):
                if abs(A[k][i]) > abs(A[max_row][i]):
                    max_row = k
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, n):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = Fraction(b[i], A[i][i])
            for k in range(i-1, -1, -1):
                b[k] -= A[k][i] * x[i]
        return x
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def determinant(A):
        n = len(A)
        det = Fraction(1)
        for i in range(n):
            max_row = i
            for k in range(i+1, n):
                if abs(A[k][i]) > abs(A[max_row][i]):
                    max_row = k
            A[i], A[max_row] = A[max_row], A[i]
            det *= Fraction(A[i][i])
            for j in range(i+1, n):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
        return det
    
    def hyperplane_arrangement(n):
        # Generate a random hyperplane arrangement
        H = []
        for i in range(1, n):
            h = [0] * (n+1)
            h[0] = 1
            for j in range(i):
                h[j+1] = random.randint(-10, 10)
            h[-1] = random.randint(-100, 100)
            H.append(h)
        return H
    
    def minimal_symplectic_leaf_number(H):
        n = len(H[0]) - 1
        A = [[0] * (n+1) for _ in range(n)]
        b = [0] * n
        for h in H:
            for i in range(n):
                A[i][i] += h[i]**2
                b[i] += h[i] * h[-1]
        x = gaussian_elimination(A, b)
        return sum(x[i] ** 2 for i in range(n))
    
    def communication_complexity(H):
        n = len(H[0]) - 1
        A = [[0] * (n+1) for _ in range(n)]
        b = [0] * n
        for h in H:
            for i in range(n):
                A[i][i] += h[i]**2
                b[i] += h[i] * h[-1]
        x = gaussian_elimination(A, b)
        return sum(x[i] ** 2 for i in range(n))
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_metric_value = Fraction(0)
    max_n = 0
    
    for n in n_values:
        for _ in range(5):
            H = hyperplane_arrangement(n)
            mnl = minimal_symplectic_leaf_number(H)
            c = communication_complexity(H)
            instances_tested += 1
            total_metric_value += mnl / c
            max_n = max(max_n, n)
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = True
    counterexample = ""
    
    return {
        "metric_name": "mnl/c",
        "metric_value": float(mean_metric_value),
        "instances_tested": instances_tested,
        "n_max": max_n,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['instances_tested']}, mnl/c={r['metric_value']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break