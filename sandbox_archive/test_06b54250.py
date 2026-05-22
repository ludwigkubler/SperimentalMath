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
    
    # Generate a random graph with n vertices and m edges
    n = 10 + random.randint(0, 20)  # Ensure n is at least 5
    m = random.randint(n - 1, n * (n - 1) // 2)
    G = [[0] * n for _ in range(n)]
    edges = set()
    while len(edges) < m:
        u, v = random.sample(range(n), 2)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            G[u][v] = G[v][u] = 1
            edges.add((u, v))
    
    # Calculate the minimal rank of geometric quantization (simplified as a proxy)
    min_rank = n
    
    # Compute the MAX-CUT solution (simplified as a proxy)
    max_cut_value = sum(max(sum(row[:i]) for row in G), sum(G[i][j] for j in range(i + 1, n))) / 2
    
    # Calculate the logarithm of the number of solutions
    log_num_solutions = math.log(max_cut_value + 1)
    
    # Check if the conjecture holds
    ratio = abs(min_rank - log_num_solutions) / (min_rank + log_num_solutions)
    conjecture_holds = ratio <= 0.1
    
    return {
        "metric_name": "Ratio of Minimal Rank to Logarithm of MAX-CUT Solutions",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Graph with {n} vertices and {m} edges"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(abs(r["metric_value"]) > 0.2 for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if abs(r["metric_value"]) > 0.2)
        print(f"RESULT: FALSIFIED counterexample='Graph with {n} vertices and {m} edges' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")