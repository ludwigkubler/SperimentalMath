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
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return edges
    
    def sdp_rank(matrix):
        singular_values = sorted([abs(e) for row in matrix for e in row], reverse=True)
        threshold = 1e-6 * singular_values[0]
        rank = sum(1 for sv in singular_values if sv > threshold)
        return rank
    
    def sos_moment_matrix(instance, d):
        n = len(instance)
        M = [[0] * (n + 1) for _ in range(n + 1)]
        for i, j in instance:
            M[i][j] += 1
            M[j][i] += 1
        return M
    
    def degree_d_sdp(matrix, d):
        n = len(matrix)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(i + 1, n):
                if matrix[i][j]:
                    A[i][i] += matrix[i][j]
                    A[j][j] += matrix[i][j]
                    A[i][j] -= matrix[i][j]
                    A[j][i] -= matrix[i][j]
        return A
    
    def solve_sdp(A):
        n = len(A)
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        P = [[0] * n for _ in range(n)]
        Q = [[0] * n for _ in range(n)]
        r = [0] * n
        for k in range(n):
            max_val = -1
            max_i, max_j = 0, 0
            for i in range(k + 1, n):
                for j in range(i + 1, n):
                    if A[i][j] > max_val:
                        max_val = A[i][j]
                        max_i, max_j = i, j
            P[k], Q[k] = I[:k+1][:k+1], I[:k+1][:k+1]
            r[k] = max_val
        return P, Q, r
    
    n = 30
    instance = generate_max_cut_instance(n)
    M2 = sos_moment_matrix(instance, 2)
    A2 = degree_d_sdp(M2, 2)
    P2, Q2, r2 = solve_sdp(A2)
    rank2 = sdp_rank(P2)
    
    M3 = sos_moment_matrix(instance, 3)
    A3 = degree_d_sdp(M3, 3)
    P3, Q3, r3 = solve_sdp(A3)
    rank3 = sdp_rank(P3)
    
    return {
        "metric_name": "SOS Moment Matrix Rank",
        "metric_value": (rank2, rank3),
        "instances_tested": 1,
        "conjecture_holds": rank2 <= 2 * math.ceil(math.sqrt(n)) and rank3 > rank2 + math.sqrt(n),
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
    
    ranks_d2 = [r["metric_value"][0] for r in results if r["instances_tested"] > 0]
    ranks_d3 = [r["metric_value"][1] for r in results if r["instances_tested"] > 0]
    
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    mean_rank_d2 = sum(ranks_d2) / len(ranks_d2)
    mean_rank_d3 = sum(ranks_d3) / len(ranks_d3)
    
    if support_fraction >= 0.8:
        result = f"RESULT: SUPPORTED mean={mean_rank_d2} std={math.sqrt(sum((x - mean_rank_d2) ** 2 for x in ranks_d2) / len(ranks_d2))} support_fraction={support_fraction}"
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        result = f"RESULT: FALSIFIED counterexample=\"rank_d2 > 2*ceil(sqrt(n)) or rank_d3 <= rank_d2 + sqrt(n)\" first_failing_seed={first_failing_seed}"
    else:
        result = "RESULT: INCONCLUSIVE mapping_undefined"
    
    print(result)