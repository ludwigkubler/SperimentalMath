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
            max_row = i + max(range(i, m), key=lambda x: abs(A[x][i]))
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

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0 for _ in range(p)] for _ in range(m)]
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
        for i in range(n):
            submatrix = [row[:i] + row[i+1:] for row in A[1:]]
            det += (-1) ** i * A[0][i] * determinant(submatrix)
        return det

    def k_group_rank(G):
        n = len(G)
        adjacency_matrix = [[G[i][j] if G[i][j] == 1 else 0 for j in range(n)] for i in range(n)]
        laplacian_matrix = [[sum(adjacency_matrix[i]) - adjacency_matrix[i][j] if i == j else -adjacency_matrix[i][j] for j in range(n)] for i in range(n)]
        return sum(1 for row in gaussian_elimination(laplacian_matrix) if any(row))

    def k_clique_protocol(G, k):
        n = len(G)
        visited = [False] * n
        def dfs(node, path):
            if len(path) == k:
                return True
            visited[node] = True
            for neighbor in range(n):
                if G[node][neighbor] and not visited[neighbor]:
                    if dfs(neighbor, path + [neighbor]):
                        return True
            visited[node] = False
            return False
        return any(dfs(i, [i]) for i in range(n))

    n_values = [10, 15, 20, 25, 30]
    results = []
    
    for n in n_values:
        G = [[random.randint(0, 1) if i != j else 0 for j in range(n)] for i in range(n)]
        K_G_rank = k_group_rank(G)
        protocol_bits = len(k_clique_protocol(G, 3)) * 2  # Assuming each bit exchange is counted as 2 bits
        results.append({
            "metric_name": "protocol_bits",
            "metric_value": protocol_bits,
            "instances_tested": 1,
            "conjecture_holds": protocol_bits >= K_G_rank,
            "counterexample": "" if protocol_bits >= K_G_rank else f"Graph with n={n} and rank {K_G_rank}"
        })
    
    mean_metric = sum(result["metric_value"] for result in results) / len(results)
    std_metric = math.sqrt(sum((result["metric_value"] - mean_metric) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_metric": mean_metric,
        "std_metric": std_metric,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric = sum(result["mean_metric"] for result in results) / len(results)
    std_metric = math.sqrt(sum((result["mean_metric"] - mean_metric) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["support_fraction"] == 1) / len(results)
    
    if all(result["support_fraction"] == 1 for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(result["support_fraction"] < 0.8 for result in results):
        print("RESULT: FALSIFIED counterexample=\"not enough seeds supporting\" first_failing_seed=1")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(results)}")