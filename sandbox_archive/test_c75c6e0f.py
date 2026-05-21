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
        n = len(A)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def trace(matrix):
        return sum(matrix[i][i] for i in range(len(matrix)))
    
    def eigenvalues(A):
        n = len(A)
        tolerance = 1e-8
        Q = [[0] * n for _ in range(n)]
        H = [[0] * n for _ in range(n)]
        
        # Compute the Hankel matrix H_G
        for i in range(n):
            for j in range(n):
                H[i][j] = (1 / n) * trace(matrix_power(A, i + j))
        
        # Perform Gaussian elimination to find the rank of H_G
        H_rank = gaussian_elimination(H)
        distinct_eigenvalues = set()
        for row in H_rank:
            if any(abs(x) > tolerance for x in row):
                distinct_eigenvalues.add(tuple(row))
        
        return len(distinct_eigenvalues)
    
    def matrix_power(matrix, power):
        n = len(matrix)
        result = [[0] * n for _ in range(n)]
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        for _ in range(power):
            result = matrix_multiply(result, matrix)
        return result
    
    def max_cut(G):
        n = len(G)
        max_cut_value = -1
        for mask in range(1 << (n - 1)):
            cut_value = sum(G[i][j] for i in range(n) for j in range(i + 1, n) if (mask & (1 << i)) and not (mask & (1 << j)))
            max_cut_value = max(max_cut_value, cut_value)
        return max_cut_value
    
    def ub_dp(G):
        n = len(G)
        min_eigenvalue = min(eigenvalues(G))
        return Fraction(n * (n - 1) // 4, 2) - Fraction(min_eigenvalue, 4)
    
    def gw_slack(G):
        n = len(G)
        ub_dp_value = ub_dp(G)
        max_cut_value = max_cut(G)
        return ub_dp_value - max_cut_value
    
    n_values = [8, 10, 12, 14, 16, 18]
    results = []
    
    for n in n_values:
        G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if G[i][j] == G[j][i]:
                    G[i][j] = G[j][i] = random.choice([0, 1])
        
        A = [[G[i][j] for j in range(n)] for i in range(n)]
        eigenvals = eigenvalues(A)
        H_G_rank = gaussian_elimination([[(1 / n) * trace(matrix_power(A, i + j)) for j in range(n)] for i in range(n)])
        distinct_eigenvalues = set()
        for row in H_G_rank:
            if any(abs(x) > 1e-8 for x in row):
                distinct_eigenvalues.add(tuple(row))
        
        if eigenvals != len(distinct_eigenvalues):
            return {
                "metric_name": "GW Slack / ν(G)",
                "metric_value": None,
                "instances_tested": 0,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        ub_dp_value = ub_dp(A)
        max_cut_value = max_cut(A)
        gw_slack_value = ub_dp_value - max_cut_value
        
        results.append(gw_slack_value / eigenvals)
    
    min_ratio = min(results)
    mean_ratio = sum(results) / len(results)
    
    return {
        "metric_name": "GW Slack / ν(G)",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": min_ratio >= 0.02 and mean_ratio <= 0.45,
        "counterexample": "" if min_ratio >= 0.02 else f"min_ratio={min_ratio}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    if all(r is not None for r in results):
        min_ratio = min(results)
        mean_ratio = sum(results) / len(results)
        support_fraction = sum(1 for r in results if r >= 0.02) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_ratio} std={sum((r - mean_ratio)**2 for r in results) / len(results)} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(i for i, r in enumerate(results) if r < 0.02)
            print(f"RESULT: FALSIFIED counterexample='min_ratio={min_ratio}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE some results are None")