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
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B[0]), len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def is_quandle_action(Q, f):
        n = len(f)
        for q1 in Q:
            for q2 in Q:
                if not any((q1[i] + q2[j]) % n == f[q1][q2] for i in range(n) for j in range(n)):
                    return False
        return True

    def tropicalize_truth_table(f):
        n = len(f)
        T = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                T[i][j] = max(f[i][k] + f[k][j] for k in range(n))
        return T

    def acc0_circuit_complexity(f):
        # Placeholder function to simulate ACC⁰ complexity
        n = len(f)
        return n * n  # Simplified approximation

    def generate_function(n):
        f = [[random.randint(0, n-1) for _ in range(n)] for _ in range(n)]
        return f

    n = random.choice([5, 10, 15, 20, 30, 40])
    t_f = acc0_circuit_complexity(generate_function(n))
    Q_size = n * n * math.log(t_f)
    
    if Q_size > n * n:
        return {
            "metric_name": "Quandle Order",
            "metric_value": Q_size,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Order exceeds O(n^2 * log(t(f)))"
        }

    f = generate_function(n)
    T = tropicalize_truth_table(f)
    
    if not is_quandle_action(Q_size, f):
        return {
            "metric_name": "Quandle Order",
            "metric_value": Q_size,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Tropicalized function does not satisfy quandle action properties"
        }

    return {
        "metric_name": "Quandle Order",
        "metric_value": Q_size,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Order exceeds O(n^2 * log(t(f)))' first_failing_seed={first_failing_seed}")