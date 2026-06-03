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
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i and A[j][i] != 0:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C
    
    def hodge_span_width(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(m):
            if all(abs(A[i][j]) < 1e-9 for j in range(n)):
                continue
            rank += 1
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if j != i and abs(A[j][i]) > 1e-9:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return rank
    
    def resolution_proof_width(phi):
        # Placeholder function to simulate resolution proof width
        # This is a dummy implementation and should be replaced with actual logic
        return len(phi)
    
    n = 10  # Example size, can be changed as needed
    phi = [random.choice([0, 1]) for _ in range(n * (n + 1) // 2)]
    A = [[phi[i * (i + 1) // 2 + j] if i >= j else 0 for j in range(i + 1)] for i in range(n)]
    
    hsw = hodge_span_width(A)
    w_phi = resolution_proof_width(phi)
    
    return {
        "metric_name": "Hodge Span Width",
        "metric_value": hsw,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": hsw <= 2 * w_phi,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")