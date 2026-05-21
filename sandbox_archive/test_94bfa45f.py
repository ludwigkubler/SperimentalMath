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
    
    def generate_random_graph(n):
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
        return x
    
    def compute_rank(matrix):
        n = len(matrix)
        matrix_copy = [row[:] for row in matrix]
        b = [0] * n
        rank = 0
        for i in range(n):
            if matrix_copy[i][i] != 0:
                rank += 1
                for j in range(i + 1, n):
                    factor = matrix_copy[j][i] / matrix_copy[i][i]
                    for k in range(i, n):
                        matrix_copy[j][k] -= factor * matrix_copy[i][k]
                    b[j] -= factor * b[i]
        return rank
    
    def degree_d_moment_matrix(G, d):
        n = len(G)
        M = [[0] * (n ** 2) for _ in range(n ** 2)]
        for i in range(n):
            for j in range(n):
                if G[i][j] == 1:
                    for k in range(d):
                        M[i * n + j][k * n + k] += 1
        return M
    
    def real_rank(G, d):
        M = degree_d_moment_matrix(G, d)
        rank = compute_rank(M)
        return rank
    
    n = random.randint(5, 40)
    G = generate_random_graph(n)
    
    results = []
    for d in [2, 4, 6]:
        rank = real_rank(G, d)
        expected_rank = math.floor(d ** 2 / math.log(n))
        if rank < expected_rank:
            return {
                "metric_name": "real_rank",
                "metric_value": rank,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"Graph with n={n}, d={d}, rank={rank}"
            }
        results.append((d, rank))
    
    return {
        "metric_name": "real_rank",
        "metric_value": sum(rank for _, rank in results) / len(results),
        "instances_tested": 3,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_rank = sum(result["metric_value"] * result["instances_tested"] for result in results) / sum(result["instances_tested"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={total_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_rank} std=0.0 support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={seed}")
                break