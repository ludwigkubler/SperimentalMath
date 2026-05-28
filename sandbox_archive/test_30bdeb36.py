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
    
    def generate_max_cut_instance(n):
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    G[i][j] = G[j][i] = random.randint(1, 10)
        return G
    
    def matrix_multiply(A, B):
        m, k, n = len(A), len(B[0]), len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for l in range(k):
                    C[i][j] += A[i][l] * B[l][j]
        return C
    
    def gaussian_elimination(A, b):
        m, n = len(A), len(A[0])
        augmented = [A[i] + [b[i]] for i in range(m)]
        for i in range(n):
            max_row = i
            for j in range(i + 1, m):
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
        A = matrix[:]
        r = 0
        for i in range(n):
            if r < m:
                max_row = r
                for j in range(r + 1, m):
                    if abs(A[j][i]) > abs(A[max_row][i]):
                        max_row = j
                A[r], A[max_row] = A[max_row], A[r]
                if A[r][i] != 0:
                    r += 1
        return r
    
    def bp_width(G):
        n = len(G)
        adj_matrix = G
        laplacian = [[0] * n for _ in range(n)]
        for i in range(n):
            degree = sum(adj_matrix[i])
            laplacian[i][i] = degree
            for j in range(i + 1, n):
                laplacian[i][j] = laplacian[j][i] = -adj_matrix[i][j]
        
        eigenvalues = gaussian_elimination(laplacian, [0] * n)
        return max(eigenvalues) - min(eigenvalues)
    
    def noncrossed_product_algebra(G):
        n = len(G)
        A = G
        B = [[G[i][j] for j in range(n)] for i in range(n)]
        C = matrix_multiply(A, B)
        return rank(C)
    
    n = random.randint(5, 40)
    instance = generate_max_cut_instance(n)
    min_rank = noncrossed_product_algebra(instance)
    bp_w = bp_width(instance)
    
    metric_name = "min_rank"
    metric_value = min_rank
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if min_rank <= 3 * bp_w:
        conjecture_holds = True
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"threshold_violation\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")