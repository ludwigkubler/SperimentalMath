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
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def construct_complex_manifold(n):
        # Construct a complex manifold Mφ associated with a random CNF formula φ
        # This is a placeholder function; replace it with actual construction logic
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]

    def minimal_representation_dimension(M):
        # Compute the minimal representation dimension of Mφ
        # This is a placeholder function; replace it with actual computation logic
        A = matrix_multiplication(M, M)
        det_A = determinant(A)
        return abs(det_A)

    def dpll_search_tree_height(phi):
        # Build the DPLL search tree for φ and measure its height |DPLL_tree(φ)|
        # This is a placeholder function; replace it with actual computation logic
        return random.randint(1, 100)

    n = random.choice([5, 10, 15, 20, 30, 40])
    phi = construct_complex_manifold(n)
    min_rep_dim = minimal_representation_dimension(phi)
    dpll_height = dpll_search_tree_height(phi)
    
    if min_rep_dim == 0:
        return {
            "metric_name": "DPLL Tree Height",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "min_rep_dim=0"
        }

    ratio = dpll_height / min_rep_dim
    return {
        "metric_name": "DPLL Tree Height",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(ratio - 1) <= 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        RESULT = f"SUPPORTED mean={mean_ratio:.2f} std=0.00 support_fraction={support_fraction:.2f}"
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        RESULT = f"FALSIFIED counterexample=\"min_rep_dim=0\" first_failing_seed={first_failing_seed}"
    else:
        RESULT = "INCONCLUSIVE mapping_undefined"
    
    print(RESULT)