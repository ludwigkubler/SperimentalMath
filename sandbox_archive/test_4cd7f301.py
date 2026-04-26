# auto-injected by SEC sandbox
import itertools
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import sys
import json
from collections import defaultdict

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def det(A):
    n = len(A)
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    else:
        det_val = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det_val += (-1) ** j * A[0][j] * det(submatrix)
        return det_val

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
            for j in range(n):
                for x in range(i, n):
                    for y in range(j, n):
                        if is_rectangle(M_f, i, j, x, y):
                            disc = abs(sum(matrix[x][y] for x in range(i, x+1) for y in range(j, y+1)))
                            max_disc = max(max_disc, disc)
        
        disc = max_disc
        
        # Compute Dgm_0 of the Hamming row/column clouds
        def hamming_distance(a, b):
            return sum(x != y for x, y in zip(a, b))
        
        rows = [''.join(str(M_f[i][j]) for j in range(n)) for i in range(n)]
        cols = [''.join(str(M_f[j][i]) for j in range(n)) for i in range(n)]
        
        def union_find(edges):
            parent = list(range(len(edges)))
            
            def find(x):
                if parent[x] != x:
                    parent[x] = find(parent[x])
                return parent[x]
            
            for u, v in edges:
                pu, pv = find(u), find(v)
                if pu != pv:
                    parent[pu] = pv
            
            components = defaultdict(list)
            for i, p in enumerate(find(i) for i in range(len(edges))):
                components[p].append(i)
            return components
        
        def bottleneck_distance(Dgm_0):
            edges = []
            for u, v in Dgm_0:
                edges.append((u, v))
            
            U = union_find(edges)
            death_times = {i: max(u, v) for i, (u, v) in enumerate(edges)}
            sorted_edges = sorted(edges, key=lambda e: death_times[e[1]])
            
            matching = [-1] * len(sorted_edges)
            visited = [False] * len(sorted_edges)
            
            def dfs(v):
                if visited[v]:
                    return False
                visited[v] = True
                for u in range(len(matching)):
                    if matching[u] == -1 and hamming_distance(rows[sorted_edges[v][0]], rows[sorted_edges[u][0]]) == 1:
                        matching[u] = v
                        matching[v] = u
                        return True
                return False
            
            max_matching_size = 0
            for i in range(len(sorted_edges)):
                if dfs(i):
                    max_matching_size += 1
            
            return len(edges) - max_matching_size
        
        Dgm_0_rows = [(i, j) for i in range(n) for j in range(n) if hamming_distance(rows[i], rows[j]) == 1]
        Dgm_0_cols = [(i, j) for i in range(n) for j in range(n) if hamming_distance(cols[i], cols[j]) == 1]
        
        d_B_rows = bottleneck_distance(Dgm_0_rows)
        d_B_cols = bottleneck_distance(Dgm_0_cols)
        d_B = max(d_B_rows, d_B_cols)
        
        # Check the inequality
        Δ = math.log2(1 / disc) - (0.5 * k - math.log(2) * d_B)
        results.append({
            "metric_name": "Δ",
            "metric_value": Δ,
            "instances_tested": 1,
            "conjecture_holds": Δ >= -0.1,
            "counterexample": "" if Δ >= -0.1 else f"Discrepancy: {disc}, Bottleneck Distance: {d_B}"
        })
    
    return {
        "metric_name": "Δ",
        "metric_value": sum(result["metric_value"] for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": next((result["counterexample"] for result in results if not result["conjecture_holds"]), "")
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {json.dumps(trial_result)}")
    
    results = [run_trial(seed) for seed in seeds]
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")