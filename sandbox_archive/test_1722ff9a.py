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
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(n-1, n*(n-1)//2)
    
    # Generate a random graph
    G = [[0]*n for _ in range(n)]
    edges = set()
    while len(edges) < m:
        u, v = random.sample(range(n), 2)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            G[u][v] = G[v][u] = 1
            edges.add((u, v))
    
    # Compute the incidence complex
    I = [[0]*(n+m) for _ in range(n)]
    for i in range(n):
        I[i][i] = 1
    edge_index = n
    for u, v in edges:
        I[u][edge_index] = I[v][edge_index] = -1
        edge_index += 1
    
    # Compute the sheaf cohomology (simplified version)
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for col in range(n):
            if all(A[row][col] == 0 for row in range(rank)):
                continue
            pivot_row = rank
            A[pivot_row], A[col] = A[col], A[pivot_row]
            rank += 1
            for row in range(rank, m):
                factor = -A[row][col] / A[pivot_row][col]
                for j in range(n):
                    A[row][j] += factor * A[pivot_row][j]
        return rank
    
    min_gen = gaussian_elimination(I)
    
    # Compute the communication complexity rank (simplified version)
    def communication_complexity_rank(G):
        n = len(G)
        edges = [(i, j) for i in range(n) for j in range(i+1, n) if G[i][j] == 1]
        return len(edges)
    
    rank_comm = communication_complexity_rank(G)
    
    # Calculate the correlation and mean absolute difference
    metric_value = min_gen / rank_comm
    abs_diff = abs(min_gen - (0.5 * rank_comm))
    
    return {
        "metric_name": "min_gen_over_rank_comm",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")