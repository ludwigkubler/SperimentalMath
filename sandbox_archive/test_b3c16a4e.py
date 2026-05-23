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
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            pivot = matrix[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                matrix[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def generate_k_clique_instance(n, k):
        edges = set()
        nodes = list(range(n))
        random.shuffle(nodes)
        for i in range(k):
            for j in range(i+1, k):
                edges.add((nodes[i], nodes[j]))
        return edges
    
    def monotone_circuit_depth(edges, n):
        # Simplified heuristic to estimate circuit depth
        return len(edges) + 2 * math.log2(n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    rank_sum = 0
    depth_sum = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            edges = generate_k_clique_instance(n, random.randint(2, min(n-1, 4)))
            matrix = [[0] * n for _ in range(n)]
            for u, v in edges:
                matrix[u][v] = 1
                matrix[v][u] = 1
            rank = gaussian_elimination(matrix)
            depth = monotone_circuit_depth(edges, n)
            rank_sum += rank
            depth_sum += depth
            instances_tested += 1
    
    mean_rank = rank_sum / instances_tested
    mean_depth = depth_sum / instances_tested
    
    conjecture_holds = mean_rank >= 1.5 * mean_depth and all(rank >= 0.5 * depth for rank, depth in zip([rank_sum] * instances_tested, [depth_sum] * instances_tested))
    
    return {
        "metric_name": "Rank vs Depth",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"mean_rank={mean_rank}, mean_depth={mean_depth}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_rank < 1.5 * mean_depth\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")