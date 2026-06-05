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
    
    def generate_graph(n, m):
        edges = set()
        while len(edges) < m:
            u = random.randint(0, n-1)
            v = random.randint(0, n-1)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        return list(edges)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                return None
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = -A[k][i]
                    for j in range(n):
                        A[k][j] += factor * A[i][j]
        return A
    
    def rank(A):
        rref = gaussian_elimination(A)
        if rref is None:
            return None
        rank = 0
        for row in rref:
            if any(row):
                rank += 1
        return rank
    
    def min_invariant_generators(G):
        n = len(G)
        incidence_matrix = [[0] * (n + 1) for _ in range(n)]
        for u, v in G:
            incidence_matrix[u][v] = 1
            incidence_matrix[v][u] = 1
            incidence_matrix[n][u] += 1
            incidence_matrix[n][v] += 1
        
        return rank(incidence_matrix)
    
    def communication_complexity_rank(G):
        n = len(G)
        max_edges = n * (n - 1) // 2
        if m > max_edges:
            return None
        
        # Simplified heuristic for demonstration purposes
        return math.ceil(math.log(m, n))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            m = random.randint(n-1, n*(n-1)//2)
            G = generate_graph(n, m)
            min_gen = min_invariant_generators(G)
            rank_comm = communication_complexity_rank(G)
            
            if min_gen is None or rank_comm is None:
                continue
            
            results.append((min_gen, rank_comm))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_gen_values = [r[0] for r in results]
    rank_comm_values = [r[1] for r in results]
    
    correlation = sum((min_gen - (sum(min_gen_values) / len(min_gen_values))) * 
                      (rank_comm - (sum(rank_comm_values) / len(rank_comm_values))) 
                      for min_gen, rank_comm in results) / len(results)
    
    abs_diffs = [abs(min_gen - rank_comm) for min_gen, rank_comm in results]
    mean_abs_diff = sum(abs_diffs) / len(abs_diffs)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) >= 0.8 and mean_abs_diff <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    std_corr = math.sqrt(sum((r["metric_value"] - mean_corr) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")