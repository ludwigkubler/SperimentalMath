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
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
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

    def rank(matrix):
        A = [row[:] for row in matrix]
        gaussian_elimination(A)
        r = 0
        for row in A:
            if any(row):
                r += 1
        return r

    def resolution_proof_length(n, rank):
        # Simplified model of resolution proof length
        return n * math.log2(rank)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        M = [[random.random() for _ in range(n)] for _ in range(n)]
        rank_M = rank(M)
        proof_length = resolution_proof_length(n, rank_M)
        
        if rank_M <= 1:
            if proof_length > n * 10:
                results.append({"n": n, "rank_M": rank_M, "proof_length": proof_length})
            else:
                return {
                    "metric_name": "resolution_proof_length",
                    "metric_value": None,
                    "instances_tested": len(n_values),
                    "conjecture_holds": False,
                    "counterexample": "mapping_undefined"
                }
        else:
            if proof_length >= 2 ** (math.log2(rank_M) * 10):
                results.append({"n": n, "rank_M": rank_M, "proof_length": proof_length})
            else:
                return {
                    "metric_name": "resolution_proof_length",
                    "metric_value": None,
                    "instances_tested": len(n_values),
                    "conjecture_holds": False,
                    "counterexample": "mapping_undefined"
                }
    
    mean_length = sum(result["proof_length"] for result in results) / len(results)
    std_length = math.sqrt(sum((result["proof_length"] - mean_length) ** 2 for result in results) / len(results))
    support_fraction = all(result["proof_length"] >= 2 ** (math.log2(result["rank_M"]) * 10) for result in results)
    
    return {
        "metric_name": "resolution_proof_length",
        "metric_value": mean_length,
        "instances_tested": len(n_values),
        "conjecture_holds": support_fraction,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **trial_result}}")
        results.append(trial_result)
    
    mean_length = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_length = math.sqrt(sum((result["metric_value"] - mean_length) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")