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

def generate_max_cut_instance(n):
    edges = []
    for i in range(n):
        for j in range(i+1, n):
            if random.random() < 0.5:
                edges.append((i, j))
    return edges

def sdp_rank(matrix):
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for col in range(n):
            pivot_row = -1
            for row in range(rank, m):
                if A[row][col] != 0:
                    pivot_row = row
                    break
            if pivot_row == -1:
                continue
            A[pivot_row], A[rank] = A[rank], A[pivot_row]
            rank += 1
            for row in range(rank, m):
                factor = A[row][col] / A[pivot_row][col]
                for j in range(n):
                    A[row][j] -= factor * A[pivot_row][j]
        return rank

    return gaussian_elimination(matrix)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [16, 25, 36]
    results_d2 = []
    results_d3 = []
    
    for n in n_values:
        for _ in range(20):
            instance = generate_max_cut_instance(n)
            # Construct degree-2 SOS moment matrix
            P2 = [[0] * (n+1) for _ in range(n+1)]
            for u, v in instance:
                P2[u][v] += 1
                P2[v][u] += 1
                P2[n][u] += 1
                P2[n][v] += 1
            rank2 = sdp_rank(P2)
            
            # Construct degree-3 SOS moment matrix
            P3 = [[0] * (n+1) for _ in range(n+1)]
            for u, v in instance:
                for w in range(n):
                    if (u, v, w) not in instance and (u, w, v) not in instance and (v, u, w) not in instance and (v, w, u) not in instance and (w, u, v) not in instance and (w, v, u) not in instance:
                        P3[u][v] += 1
                        P3[v][u] += 1
                        P3[w][u] += 1
                        P3[w][v] += 1
            rank3 = sdp_rank(P3)
            
            results_d2.append(rank2)
            results_d3.append(rank3)
    
    mean_rank_d2 = sum(results_d2) / len(results_d2)
    mean_rank_d3 = sum(results_d3) / len(results_d3)
    
    conjecture_holds = (mean_rank_d2 <= 2 * math.ceil(math.sqrt(n_values[0])) and
                        mean_rank_d3 > mean_rank_d2 + math.sqrt(n_values[0]))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Rank",
        "metric_value": (mean_rank_d2, mean_rank_d3),
        "instances_tested": len(results_d2) + len(results_d3),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [i for i in range(2, 50, 2)]
    
    results_d2_total = []
    results_d3_total = []
    conjecture_holds_count = 0
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        
        if result["conjecture_holds"]:
            conjecture_holds_count += 1
        results_d2_total.extend(result["metric_value"][0] for _ in range(40))
        results_d3_total.extend(result["metric_value"][1] for _ in range(40))
    
    mean_rank_d2 = sum(results_d2_total) / len(results_d2_total)
    mean_rank_d3 = sum(results_d3_total) / len(results_d3_total)
    support_fraction = conjecture_holds_count / len(seeds)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank_d2:.4f} std={math.sqrt(sum((x - mean_rank_d2)**2 for x in results_d2_total) / len(results_d2_total)):.4f} support_fraction={support_fraction:.4f}")
    elif any(result["conjecture_holds"] == False for result in results):
        first_failing_seed = seeds[next(i for i, result in enumerate(results) if not result["conjecture_holds"])]
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")