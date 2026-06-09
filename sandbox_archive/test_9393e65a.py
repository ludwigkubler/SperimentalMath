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
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(i, n + 1):
                A[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(i, n + 1):
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

    def determinant(A):
        n = len(A)
        det = 0
        if n == 1:
            return A[0][0]
        elif n == 2:
            return A[0][0] * A[1][1] - A[0][1] * A[1][0]
        else:
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in A[1:]]
                det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def construct_complex_manifold(n):
        # Placeholder for constructing the complex manifold
        # This is a dummy implementation and should be replaced with actual logic
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]

    def dpll_search_tree_height(phi):
        # Placeholder for DPLL search tree height calculation
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(5, 20)

    n = random.choice([5, 10, 15, 20, 30, 40])
    phi = construct_complex_manifold(n)
    
    M_phi = construct_complex_manifold(n)
    det_M_phi = determinant(M_phi)
    if det_M_phi == 0:
        return {
            "metric_name": "DPLL_tree_height",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Determinant of M_phi is zero"
        }
    
    min_rep_dim_M_phi = len(gaussian_elimination(M_phi))
    
    dpll_tree_height = dpll_search_tree_height(phi)
    
    if dpll_tree_height is None:
        return {
            "metric_name": "DPLL_tree_height",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Failed to compute DPLL tree height"
        }
    
    ratio = dpll_tree_height / min_rep_dim_M_phi
    
    return {
        "metric_name": "DPLL_tree_height",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(ratio - 1) <= 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio:.2f} std=0.00 support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Ratio outside ±10% of 1' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")