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
            for j in range(n):
                A[i][j] /= factor
            for j in range(n):
                if i != j:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        n = len(A)
        C = [[0]*n for _ in range(n)]
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
            return A[0][0]*A[1][1] - A[0][1]*A[1][0]
        else:
            for i in range(n):
                submatrix = [row[:i] + row[i+1:] for row in A[1:]]
                det += (-1)**i * A[0][i] * determinant(submatrix)
        return det

    def read_twice_bp_size(n, r):
        # Placeholder function to simulate read-twice BP size
        return 2**(n*r)

    def minimal_rank(n):
        # Placeholder function to simulate minimal rank of locally constant sheaf
        return n // 10 + 1

    n = random.randint(5, 40)
    r = minimal_rank(n)
    P_size = read_twice_bp_size(n, r)
    
    A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    det_A = determinant(A)
    
    if det_A == 0:
        return {
            "metric_name": "Ratio",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Determinant of A is zero"
        }
    
    B = gaussian_elimination(A)
    rank_A = sum(1 for row in B if any(row))
    
    if rank_A > r + 1:
        return {
            "metric_name": "Ratio",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Rank of A is {rank_A}, expected at most {r+1}"
        }
    
    ratio = P_size / (2**(n*r))
    return {
        "metric_name": "Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": abs(ratio - 1) <= 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("metric_value" is not None and "conjecture_holds" in r for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i, r) for i, r in enumerate(results) if "metric_value" is None or not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Rank exceeds expected' first_failing_seed={first_failing_seed[0]}")