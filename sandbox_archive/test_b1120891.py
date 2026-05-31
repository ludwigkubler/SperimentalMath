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
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            factor = A[i][i]
            for j in range(i, n + 1):
                A[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(i, n + 1):
                        A[j][k] -= factor * A[i][k]
        return [row[-1] for row in A]

    def communication_complexity(G):
        n = len(G)
        visited = [False] * n
        queue = [0]
        visited[0] = True
        complexity = 0
        while queue:
            next_queue = []
            for u in queue:
                for v in range(n):
                    if G[u][v] and not visited[v]:
                        visited[v] = True
                        next_queue.append(v)
                        complexity += 1
            queue = next_queue
        return complexity

    def minimal_local_system_rank(G):
        n = len(G)
        vertices = list(range(n))
        random.shuffle(vertices)
        A = [[0 for _ in range(n)] for _ in range(n)]
        for u, v in G:
            A[u][v] = 1
            A[v][u] = 1
        rank = gaussian_elimination(A)
        return sum(rank)

    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    complexities = []
    
    for n in n_values:
        G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            G[i][i] = 0
        rank = minimal_local_system_rank(G)
        complexity = communication_complexity(G)
        ranks.append(rank)
        complexities.append(complexity)

    if len(ranks) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(ranks),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    correlation = sum((ranks[i] - mean_ranks) * (complexities[i] - mean_complexities) for i in range(len(ranks))) / len(ranks)
    mean_ranks = sum(ranks) / len(ranks)
    mean_complexities = sum(complexities) / len(complexities)

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation,
        "instances_tested": len(ranks),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_ranks = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_ranks = math.sqrt(sum((r["metric_value"] - mean_ranks)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ranks} std={std_ranks} support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_ranks} std={std_ranks} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={result['seed']}")
                break