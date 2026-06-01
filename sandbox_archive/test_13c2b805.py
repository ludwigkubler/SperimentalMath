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
    
    def generate_bipartite_graph(n, Δ):
        A = set(range(n // 2))
        B = set(range(n // 2, n))
        edges = []
        for u in A:
            for v in B:
                if len(edges) >= Δ * (n // 2):
                    break
                edges.append((u, v))
        return A, B, edges
    
    def generate_tropical_curve(A, B, edges):
        T = {u: {} for u in A}
        for u in A:
            for v in B:
                T[u][v] = 0
        for u, v in edges:
            T[u][v] += 1
        return T
    
    def communication_complexity_rank(G):
        n = len(G)
        rank = 0
        for i in range(n):
            neighbors = set()
            for j in range(i + 1, n):
                if (i, j) in G or (j, i) in G:
                    neighbors.add(j)
            rank += len(neighbors)
        return rank
    
    def hodge_arcs_count(T):
        count = 0
        for u in T:
            for v in T[u]:
                count += T[u][v]
        return count
    
    n_values = [5, 10, 15, 20, 30, 40]
    hodge_counts = []
    comm_ranks = []
    
    for n in n_values:
        Δ = random.randint(1, min(n // 2 - 1, 10))
        A, B, edges = generate_bipartite_graph(n, Δ)
        T = generate_tropical_curve(A, B, edges)
        hodge_count = hodge_arcs_count(T)
        comm_rank = communication_complexity_rank(edges)
        hodge_counts.append(hodge_count)
        comm_ranks.append(comm_rank)
    
    mean_hodge_count = sum(hodge_counts) / len(hodge_counts)
    mean_comm_rank = sum(comm_ranks) / len(comm_ranks)
    ratio_mean = mean_hodge_count / mean_comm_rank
    
    conjecture_holds = 0.1 < ratio_mean < 2
    counterexample = "" if conjecture_holds else f"Ratio {ratio_mean} out of bounds"
    
    return {
        "metric_name": "Hodge Arcs vs Communication Complexity Rank",
        "metric_value": ratio_mean,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.1 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0.1)
        print(f"RESULT: FALSIFIED counterexample=\"Ratio too low\" first_failing_seed={first_failing_seed}")
    elif any(not r["conjecture_holds"] and r["metric_value"] > 2 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] > 2)
        print(f"RESULT: FALSIFIED counterexample=\"Ratio too high\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")