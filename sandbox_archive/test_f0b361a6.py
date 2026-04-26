# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + A[i:].index(max(abs(row[i]) for row in A[i:]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    if len(A) == 1:
        return A[0][0]
    det = 0
    for i in range(len(A)):
        submatrix = [row[:i] + row[i+1:] for row in A[1:]]
        det += (-1)**i * A[0][i] * determinant(submatrix)
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    k_values = [2, 3]
    if seed % 5 == 0:
        k_values.append(4)
    
    results = []
    for k in k_values:
        n = 2 ** k
        M_f = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
        
        # Compute discrepancy disc(M_f)
        def is_rectangle(matrix, x1, y1, x2, y2):
            return all(matrix[x][y] == matrix[x1][y1] for x in range(x1, x2+1) for y in range(y1, y2+1))
        
        max_disc = 0
        for i in range(n):
            for j in range(i+1, n):
                for x1 in range(n):
                    for y1 in range(n):
                        for x2 in range(x1, n):
                            for y2 in range(y1, n):
                                if is_rectangle(M_f, x1, y1, x2, y2) and is_rectangle(M_f, i, j, x2, y2):
                                    disc = abs(sum(matrix[x][y] for x in range(x1, x2+1) for y in range(y1, y2+1)))
                                    max_disc = max(max_disc, disc)
        
        disc = 1 / max_disc
        
        # Compute Hamming row/column clouds
        rows = [[i // n, i % n] for i in range(n * n)]
        cols = [[i % n, i // n] for i in range(n * n)]
        
        def union_find(edges):
            parent = list(range(len(edges)))
            rank = [0] * len(edges)
            
            def find(x):
                if parent[x] != x:
                    parent[x] = find(parent[x])
                return parent[x]
            
            def union(x, y):
                rootX = find(x)
                rootY = find(y)
                if rootX != rootY:
                    if rank[rootX] > rank[rootY]:
                        parent[rootY] = rootX
                    elif rank[rootX] < rank[rootY]:
                        parent[rootX] = rootY
                    else:
                        parent[rootY] = rootX
                        rank[rootX] += 1
            
            for u, v in edges:
                union(u, v)
            
            return parent
        
        def bottleneck_distance(parent):
            death_times = [0] * len(parent)
            for i in range(len(parent)):
                if parent[i] == i:
                    death_times[i] = sum(1 for j in range(i+1, len(parent)) if find(j) == i)
            
            edges = []
            for u, v in enumerate(death_times):
                edges.append((u, v))
            
            return max(v - u for u, v in edges)
        
        row_edges = sorted([(rows[i][0], rows[i][1]) for i in range(n * n)])
        col_edges = sorted([(cols[i][0], cols[i][1]) for i in range(n * n)])
        
        row_parent = union_find(row_edges)
        col_parent = union_find(col_edges)
        
        d_B_row = bottleneck_distance(row_parent)
        d_B_col = bottleneck_distance(col_parent)
        
        d_B = max(d_B_row, d_B_col)
        
        # Check the inequality
        lhs = math.log2(1 / disc)
        rhs = 0.5 * k - math.log(2) * d_B
        
        results.append({
            "metric_name": "log_disc_minus_bound",
            "metric_value": lhs - rhs,
            "instances_tested": 1,
            "conjecture_holds": lhs >= rhs,
            "counterexample": ""
        })
    
    return {
        "seed": seed,
        "trials": results
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    all_results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.extend(result["trials"])
    
    mean_delta = sum(res["metric_value"] for res in all_results) / len(all_results)
    support_fraction = sum(1 for res in all_results if res["conjecture_holds"]) / len(all_results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_delta} std=NA support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in all_results):
        first_failing_seed = seeds[all_results.index(next(res for res in all_results if not res["conjecture_holds"]))["seed"]]
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")