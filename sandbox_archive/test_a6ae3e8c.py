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
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = -A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] += factor * A[i][k]
        return A

    def matrix_mult(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def matrix_power(A, n):
        result = [[Fraction(1) if i == j else Fraction(0) for j in range(len(A))] for i in range(len(A))]
        while n > 0:
            if n % 2 == 1:
                result = matrix_mult(result, A)
            A = matrix_mult(A, A)
            n //= 2
        return result

    def resolution_width(phi_G):
        # Simplified example of resolution width calculation
        # This is a placeholder and should be replaced with actual logic
        return len(phi_G) ** 0.5

    def minimal_generator_order(kac_moody_algebra):
        # Simplified example of minimal generator order calculation
        # This is a placeholder and should be replaced with actual logic
        return len(kac_moody_algebra) ** 0.5

    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    
    for n in n_values:
        phi_G = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        w_phi_G = resolution_width(phi_G)
        order = minimal_generator_order(phi_G)
        metrics.append({"n": n, "w_phi_G": w_phi_G, "order": order})
    
    if len(metrics) < 30:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": len(metrics),
            "n_max": max(m["n"] for m in metrics),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    correlation_coefficient = 0
    n_values = [m["n"] for m in metrics]
    w_phi_Gs = [m["w_phi_G"] for m in metrics]
    orders = [m["order"] for m in metrics]
    
    mean_n = sum(n_values) / len(n_values)
    mean_w_phi_G = sum(w_phi_Gs) / len(w_phi_Gs)
    mean_order = sum(orders) / len(orders)
    
    numerator = sum((n - mean_n) * (w_phi_G - mean_w_phi_G) for n, w_phi_G in zip(n_values, w_phi_Gs))
    denominator = math.sqrt(sum((n - mean_n) ** 2 for n in n_values)) * math.sqrt(sum((w_phi_G - mean_w_phi_G) ** 2 for w_phi_G in w_phi_Gs))
    
    if denominator == 0:
        correlation_coefficient = None
    else:
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "resolution_width",
        "metric_value": correlation_coefficient,
        "instances_tested": len(metrics),
        "n_max": max(m["n"] for m in metrics),
        "conjecture_holds": correlation_coefficient is not None and 0.5 <= correlation_coefficient < 0.8,
        "counterexample": "" if correlation_coefficient is not None else "correlation_coefficient=0"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient=0' first_failing_seed={first_failing_seed}")