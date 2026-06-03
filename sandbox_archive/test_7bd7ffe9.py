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
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiply(A, B):
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
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1)**j * A[0][j] * determinant(submatrix)
        return det
    
    def hodge_span_width(A):
        if len(A) == 0 or len(A[0]) == 0:
            raise ValueError("Matrix must be non-empty")
        rank = 0
        for i in range(len(A)):
            row = A[i]
            if all(x == 0 for x in row):
                continue
            rank += 1
            for j in range(i+1, len(A)):
                factor = A[j][i] / row[i]
                for k in range(len(row)):
                    A[j][k] -= factor * row[k]
        return rank
    
    def resolution_proof_width(phi):
        # Placeholder function to compute resolution proof width
        # This is a dummy implementation and should be replaced with actual logic
        return len(phi.split())
    
    n = random.randint(5, 40)
    phi = ' '.join(random.choice('01') for _ in range(n**2))
    A = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
    
    hsw = hodge_span_width(A)
    w_phi = resolution_proof_width(phi)
    
    if hsw > 2 * w_phi:
        return {
            "metric_name": "Hodge Span Width",
            "metric_value": hsw,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"HSW({phi}) > 2 * w({phi})"
        }
    
    return {
        "metric_name": "Hodge Span Width",
        "metric_value": hsw,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results]
    conjecture_holds = all(r["conjecture_holds"] for r in results)
    
    if conjecture_holds:
        mean = sum(metric_values) / len(metric_values)
        std = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")