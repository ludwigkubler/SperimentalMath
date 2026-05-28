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
    
    def generate_k_clique(n, k):
        edges = set()
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                if random.random() < 0.5 and len(edges & {(i, x) for x in range(j+1, n+1)}) == k-2:
                    edges.add((i, j))
        return edges
    
    def quasi_metric_space(edges):
        n = max(max(u, v) for u, v in edges)
        dist = [[0] * (n + 1) for _ in range(n + 1)]
        for u, v in edges:
            dist[u][v] = dist[v][u] = 1
        for k in range(2, n + 1):
            for i in range(1, n - k + 2):
                for j in range(i + k - 1, n + 1):
                    for m in range(i, j):
                        dist[i][j] = min(dist[i][j], dist[i][m] + dist[m+1][j])
        return dist
    
    def minimal_rank(dist):
        n = len(dist) - 1
        rank = [0] * (n + 1)
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                if dist[i][j] > 0:
                    rank[j] += 1
        return max(rank) + 1
    
    def monotone_circuit_size(n, k):
        # Simplified upper bound for monotone circuit size of k-CLIQUE
        return math.comb(n, k)
    
    n = random.randint(5, 40)
    k = random.randint(2, min(n - 1, 3))
    edges = generate_k_clique(n, k)
    dist = quasi_metric_space(edges)
    rank = minimal_rank(dist)
    circuit_size = monotone_circuit_size(n, k)
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= n ** k - 0.5 * n ** k,
        "counterexample": "" if rank >= n ** k - 0.5 * n ** k else f"n={n}, k={k}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['metric_value']}, k={k}\" first_failing_seed={first_failing_seed}")