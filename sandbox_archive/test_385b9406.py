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

def generate_random_graph(n):
    edges = set()
    for _ in range(int(n * (n - 1) / 2)):
        u, v = random.sample(range(n), 2)
        if u < v:
            edges.add((u, v))
    return edges

def kronecker_dimension(edges):
    n = len(edges)
    if n == 0:
        return 0
    A = [[Fraction(1, n)] * n for _ in range(n)]
    for u, v in edges:
        A[u][v] = Fraction(0, 1)
        A[v][u] = Fraction(0, 1)
    rank = 0
    for i in range(n):
        if all(A[j][i] == Fraction(0, 1) for j in range(i)):
            continue
        pivot_row = next(j for j in range(i, n) if A[j][i] != Fraction(0, 1))
        A[i], A[pivot_row] = A[pivot_row], A[i]
        rank += 1
        for j in range(n):
            if j == i:
                continue
            factor = A[j][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return rank

def minimal_rank(edges):
    n = len(edges)
    if n == 0:
        return 0
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    visited = [False] * n
    rank = 0
    for i in range(n):
        if not visited[i]:
            stack = [i]
            while stack:
                node = stack.pop()
                if not visited[node]:
                    visited[node] = True
                    rank += 1
                    for neighbor in graph[node]:
                        if not visited[neighbor]:
                            stack.append(neighbor)
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        edges = generate_random_graph(n)
        kronecker_dim = kronecker_dimension(edges)
        min_rank = minimal_rank(edges)
        if min_rank == 0:
            continue
        c = Fraction(kronecker_dim, min_rank)
        results.append((kronecker_dim, c))
    if not results:
        return {
            "metric_name": "Kronecker Dimension",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    mean = sum(k for k, _ in results) / len(results)
    std_dev = math.sqrt(sum((k - mean) ** 2 for k, _ in results) / len(results))
    c_values = [c for _, c in results]
    support_fraction = sum(1 for c in c_values if c <= Fraction(mean, 5)) / len(c_values)
    return {
        "metric_name": "Kronecker Dimension",
        "metric_value": mean,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"kronecker_dim={mean}, c*min_rank={c_values[0]*min_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")