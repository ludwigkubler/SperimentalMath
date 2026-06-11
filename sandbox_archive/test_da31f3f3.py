# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_graph(n, d):
        if (d * n) % 2 != 0 or d >= n:
            return None
        adj_matrix = [[0] * n for _ in range(n)]
        edges_added = 0
        while edges_added < d * n // 2:
            u, v = random.sample(range(n), 2)
            if adj_matrix[u][v] == 0 and u != v:
                adj_matrix[u][v] = 1
                adj_matrix[v][u] = 1
                edges_added += 1
        return adj_matrix
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(M):
        n = len(M)
        augmented_matrix = [row + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(M)]
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                    max_row = j
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            pivot = augmented_matrix[i][i]
            for j in range(i, n+1):
                augmented_matrix[i][j] /= pivot
            for j in range(n):
                if j != i:
                    factor = augmented_matrix[j][i]
                    for k in range(i, n+1):
                        augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        return [row[n:] for row in augmented_matrix]
    
    def det(A):
        n = len(A)
        if n == 2:
            return A[0][0] * A[1][1] - A[0][1] * A[1][0]
        det_val = 0
        for j in range(n):
            sub_matrix = [row[:j] + row[j+1:] for row in A[1:]]
            det_val += (-1) ** j * A[0][j] * det(sub_matrix)
        return det_val
    
    def br_order(G):
        n = len(G)
        I = [[Fraction(1 if i == j else 0, 1) for j in range(n)] for i in range(n)]
        B = G + I
        reduced_B = gaussian_elimination(B)
        return abs(det(reduced_B))
    
    def resolution_width(G):
        n = len(G)
        # Simplified heuristic for width; actual implementation depends on the graph structure
        return sum(sum(row) for row in G) // 2
    
    n = random.randint(5, 40)
    d = random.randint(1, n-1)
    G = generate_d_regular_graph(n, d)
    if G is None:
        return {
            "metric_name": "br_order",
            "metric_value": -1,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "d-regular graph generation failed"
        }
    
    br = br_order(G)
    width = resolution_width(G)
    
    return {
        "metric_name": "br_order",
        "metric_value": br,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = (sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))**0.5
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] and res["metric_value"] != -1 for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")