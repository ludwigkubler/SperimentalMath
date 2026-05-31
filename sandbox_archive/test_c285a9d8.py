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
    
    def generate_graph(n, max_degree):
        G = [[] for _ in range(n)]
        edges = set()
        while len(edges) < n * max_degree // 2:
            u, v = random.sample(range(n), 2)
            if (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
                G[u].append(v)
                G[v].append(u)
        return G
    
    def communication_complexity(G):
        n = len(G)
        cc = 0
        for i in range(n):
            cc += len(G[i])
        return cc / n
    
    def minimal_local_system_rank(G):
        n = len(G)
        if n == 1:
            return 1
        rank = 0
        for u in range(n):
            neighbors = G[u]
            if not neighbors:
                continue
            A = [[0] * (len(neighbors) + 1) for _ in range(len(neighbors) + 1)]
            for j, v in enumerate(neighbors):
                A[j][j] = 1
                for k, w in enumerate(G[v]):
                    if w != u and w not in neighbors:
                        A[j][k + len(neighbors)] = 1
            rank += gaussian_elimination(A)
        return rank
    
    def gaussian_elimination(A):
        n = len(A)
        rank = 0
        for i in range(n):
            pivot_row = -1
            for j in range(i, n):
                if A[j][i] != 0:
                    pivot_row = j
                    break
            if pivot_row == -1:
                continue
            rank += 1
            for j in range(n):
                A[i][j], A[pivot_row][j] = A[pivot_row][j], A[i][j]
            for j in range(n):
                if i != j and A[j][i] != 0:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_rank = 0.0
    total_cc = 0.0
    
    for n in n_values:
        for _ in range(5):
            G = generate_graph(n, 3)
            rank = minimal_local_system_rank(G)
            cc = communication_complexity(G)
            instances_tested += 1
            total_rank += rank
            total_cc += cc
    
    mean_rank = total_rank / instances_tested
    mean_cc = total_cc / instances_tested
    correlation_coefficient = (instances_tested * total_rank * total_cc - 
                               sum(rank * cc for rank, cc in zip(ranks, ccs))) / \
                              math.sqrt((instances_tested * sum(rank**2 for rank in ranks) - sum(rank**2 for rank in ranks)) *
                                        (instances_tested * sum(cc**2 for cc in ccs) - sum(cc**2 for cc in ccs)))
    
    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.7"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
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
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")