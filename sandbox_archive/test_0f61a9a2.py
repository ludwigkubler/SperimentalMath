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
            # Find pivot
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            
            # Eliminate
            for j in range(m):
                if i != j:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0]*p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        
        det = 0
        if n == 1:
            return A[0][0]
        elif n == 2:
            return A[0][0] * A[1][1] - A[0][1] * A[1][0]
        else:
            for j in range(n):
                det += ((-1)**j) * A[0][j] * determinant([row[:j] + row[j+1:] for row in A[1:]])
        return det

    def hyperplane_arrangement_complexity(hyperplanes):
        # Simplified complexity measure based on the number of intersections
        m, n = len(hyperplanes), len(hyperplanes[0])
        intersection_matrix = [[0]*n for _ in range(n)]
        for i in range(m):
            for j in range(i+1, m):
                if hyperplanes[i][j] != 0 and hyperplanes[j][i] != 0:
                    intersection_matrix[i][j], intersection_matrix[j][i] = 1, 1
        return determinant(intersection_matrix)

    def communication_complexity(instance):
        # Simplified complexity measure based on the length of the instance
        return len(instance)

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            instance = [random.choice([-1, 1]) for _ in range(n)]
            hyperplanes = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
            mnl = hyperplane_arrangement_complexity(hyperplanes)
            c = communication_complexity(instance)
            results.append((instance, (mnl, c)))

    if not results:
        return {
            "metric_name": "minimal_symplectic_leaf_number",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    mnl_values = [mnl for _, (mnl, _) in results]
    c_values = [c for _, (_, c) in results]

    n_max = max([len(instance) for instance, _ in results])
    
    if len(mnl_values) < 30 or n_max < 16:
        return {
            "metric_name": "minimal_symplectic_leaf_number",
            "metric_value": 0,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }

    correlation = sum((mnl - mnl_mean) * (c - c_mean) for mnl, c in zip(mnl_values, c_values)) / len(results)
    mnl_std = math.sqrt(sum((mnl - mnl_mean)**2 for mnl in mnl_values) / len(results))
    c_std = math.sqrt(sum((c - c_mean)**2 for c in c_values) / len(results))

    if correlation >= 0.8:
        return {
            "metric_name": "minimal_symplectic_leaf_number",
            "metric_value": correlation,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "minimal_symplectic_leaf_number",
            "metric_value": correlation,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": f"correlation={correlation:.2f} < 0.8"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std={std_metric_value:.4f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std={std_metric_value:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation < 0.8\" first_failing_seed={first_failing_seed}")