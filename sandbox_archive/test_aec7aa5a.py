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
    
    def generate_boolean_function_graph(n):
        G = []
        for i in range(2**n):
            G.append([i ^ j for j in range(i+1)])
        return G
    
    def min_affine_generators(G):
        m = len(G)
        n = int(math.log2(m))
        A = [[0]*n for _ in range(m)]
        b = [0]*m
        
        for i, g in enumerate(G):
            for j in range(n):
                if (1 << j) & i:
                    A[i][j] = 1
                else:
                    A[i][j] = -1
            b[i] = 1
        
        # Gaussian elimination to find the rank of matrix A
        def gaussian_elimination(A, b):
            m, n = len(A), len(A[0])
            for i in range(m):
                max_row = i
                for j in range(i+1, m):
                    if abs(A[j][i]) > abs(A[max_row][i]):
                        max_row = j
                A[i], A[max_row] = A[max_row], A[i]
                b[i], b[max_row] = b[max_row], b[i]
                
                for j in range(i+1, m):
                    factor = -A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] += factor * A[i][k]
                    b[j] += factor * b[i]
            
            rank = 0
            for i in range(m):
                if any(A[i][j] != 0 for j in range(n)):
                    rank += 1
            return rank
        
        rank = gaussian_elimination(A, b)
        return rank
    
    def communication_complexity(G):
        n = int(math.log2(len(G)))
        return n + 1
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        G = generate_boolean_function_graph(n)
        m_G = min_affine_generators(G)
        comm_complexity = communication_complexity(G)
        
        if m_G == 0 or comm_complexity == 0:
            continue
        
        results.append((m_G, comm_complexity))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    m_G_values = [m for m, _ in results]
    comm_complexity_values = [c for _, c in results]
    
    mean_ranks = sum(m_G_values) / len(m_G_values)
    std_dev = math.sqrt(sum((x - mean_ranks)**2 for x in m_G_values) / len(m_G_values))
    correlation_coefficient = sum((m_G_values[i] - mean_ranks) * (comm_complexity_values[i] - sum(comm_complexity_values)/len(comm_complexity_values)) for i in range(len(m_G_values))) / (len(m_G_values) * std_dev * math.sqrt(sum((c - sum(comm_complexity_values)/len(comm_complexity_values))**2 for c in comm_complexity_values)))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ranks = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(mean_ranks)/len(mean_ranks)} std={math.sqrt(sum((x - sum(mean_ranks)/len(mean_ranks))**2 for x in mean_ranks)/len(mean_ranks))} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(mean_ranks)/len(mean_ranks)} std={math.sqrt(sum((x - sum(mean_ranks)/len(mean_ranks))**2 for x in mean_ranks)/len(mean_ranks))} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")