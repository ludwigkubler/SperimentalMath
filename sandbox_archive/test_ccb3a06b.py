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
    
    n = 20
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    
    def matrix_multiplication(A, B):
        m, k, n = len(A), len(B[0]), len(B)
        result = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for l in range(k):
                    result[i][j] += A[i][l] * B[l][j]
        return result
    
    def gaussian_elimination(A, b):
        m, n = len(A), len(A[0])
        augmented = [A[i] + [b[i]] for i in range(m)]
        for i in range(n):
            max_row = i
            for j in range(i+1, m):
                if abs(augmented[j][i]) > abs(augmented[max_row][i]):
                    max_row = j
            augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
            pivot = augmented[i][i]
            for j in range(n + 1):
                augmented[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = augmented[j][i]
                    for k in range(n + 1):
                        augmented[j][k] -= factor * augmented[i][k]
        return [row[-1] for row in augmented]
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        A = matrix
        r = min(m, n)
        for i in range(r):
            if A[i][i] == 0:
                swap_found = False
                for j in range(i+1, m):
                    if A[j][i] != 0:
                        A[i], A[j] = A[j], A[i]
                        swap_found = True
                        break
                if not swap_found:
                    r -= 1
            else:
                for j in range(m):
                    if j != i:
                        factor = A[j][i] / A[i][i]
                        for k in range(n):
                            A[j][k] -= factor * A[i][k]
        return r
    
    M_d = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            M_d[i][j] = sum(G[k][i] * G[k][j] for k in range(n))
            M_d[j][i] = M_d[i][j]
    
    rank_M_d = rank(M_d)
    sqrt_n = math.sqrt(n)
    
    return {
        "metric_name": "rank(M_d)",
        "metric_value": rank_M_d,
        "instances_tested": 1,
        "conjecture_holds": rank_M_d >= sqrt_n,
        "counterexample": "" if rank_M_d >= sqrt_n else f"Rank of M_d ({rank_M_d}) is less than √n ({sqrt_n})"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank(M_d) < √n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")