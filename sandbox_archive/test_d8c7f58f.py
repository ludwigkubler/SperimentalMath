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
    
    def generate_bipartite_graph(n, delta):
        A = [set() for _ in range(n)]
        B = [set() for _ in range(n)]
        edges = set()
        
        for i in range(n):
            for j in range(n):
                if len(A[i]) < delta and len(B[j]) < delta:
                    if random.choice([True, False]):
                        A[i].add(j)
                        B[j].add(i)
                        edges.add((i, j))
        
        return A, B, edges
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i + 1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            pivot = matrix[i][i]
            for j in range(cols):
                matrix[i][j] /= pivot
            
            for j in range(rows):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
        
        return matrix
    
    def communication_complexity_rank(G):
        n = len(G)
        total_edges = sum(len(neighbors) for neighbors in G)
        return total_edges / n
    
    def minimal_hodge_arcs(A, B, edges):
        n = len(A)
        H = [[0] * n for _ in range(n)]
        
        for u, v in edges:
            if u < v:
                H[u][v] += 1
                H[v][u] += 1
        
        rank = gaussian_elimination(H)
        return sum(sum(row) for row in rank)
    
    def generate_seeds():
        seeds = []
        for i in range(2, 30):
            if i % 2 == 0:
                seeds.append(i)
        return seeds
    
    seeds = generate_seeds()
    metric_values = []
    instances_tested = 0
    n_max = 0
    
    for n in seeds:
        delta = random.randint(1, min(n - 1, 5))
        A, B, edges = generate_bipartite_graph(n, delta)
        
        if not edges:
            continue
        
        instances_tested += 1
        n_max = max(n_max, n)
        
        hodge_arcs = minimal_hodge_arcs(A, B, edges)
        rank = communication_complexity_rank([A, B])
        
        metric_values.append(hodge_arcs / rank)
    
    if not metric_values:
        return {
            "metric_name": "Hodge Arcs to Rank Ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No valid bipartite graph generated"
        }
    
    mean_ratio = sum(metric_values) / len(metric_values)
    conjecture_holds = all(0.1 <= ratio < 2 for ratio in metric_values)
    
    return {
        "metric_name": "Hodge Arcs to Rank Ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(r["metric_value"] < 0.1 or r["metric_value"] > 2 for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if r["metric_value"] < 0.1 or r["metric_value"] > 2)
        print(f"RESULT: FALSIFIED counterexample=\"Ratio out of bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")