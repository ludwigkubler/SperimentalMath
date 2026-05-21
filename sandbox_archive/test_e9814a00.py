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

def random_matrix(n):
    return [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]

def hamming_distance(a, b):
    return sum(x != y for x, y in zip(a, b))

def kruskal(edges, n):
    parent = list(range(n))
    rank = [0] * n

    def find(i):
        if parent[i] != i:
            parent[i] = find(parent[i])
        return parent[i]

    def union(x, y):
        rootX = find(x)
        rootY = find(y)

        if rootX != rootY:
            if rank[rootX] > rank[rootY]:
                parent[rootY] = rootX
            elif rank[rootX] < rank[rootY]:
                parent[rootX] = rootY
            else:
                parent[rootY] = rootX
                rank[rootX] += 1

    edges.sort(key=lambda x: x[2])
    mst_edges = []
    for u, v, weight in edges:
        if find(u) != find(v):
            union(u, v)
            mst_edges.append((u, v, weight))
    return mst_edges

def persistence_entropy(M):
    n = len(M)
    distances = [hamming_distance(M[i], M[j]) for i in range(n) for j in range(i + 1, n)]
    weights = sorted([d for d in distances if d > 0])
    L = sum(weights)
    pe = -sum((w / L) * math.log2(w / L) for w in weights)
    return pe

def rank_real(M):
    n = len(M)
    M_copy = [row[:] for row in M]
    u, s, vh = [], [], []
    for _ in range(n):
        max_col = max(range(n), key=lambda j: abs(M_copy[j][0]))
        u.append([M_copy[i][max_col] / M_copy[0][max_col] if i == 0 else M_copy[i][max_col] for i in range(n)])
        M_copy[0], M_copy[max_col] = M_copy[max_col], M_copy[0]
        s.append(M_copy[0][0])
        M_copy = [[M_copy[j][k] / M_copy[0][k] if k > 0 else M_copy[j][k] for k in range(n)] for j in range(1, n)]
    return len(s)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [8, 16, 24, 32]:
        for _ in range(5):
            if n == 8 and _ >= 2:
                continue
            M = random_matrix(n)
            pe = persistence_entropy(M)
            rank = rank_real(M)
            results.append((n, pe, rank))
    total_pe = sum(pe for _, pe, _ in results)
    total_rank = sum(rank for _, _, rank in results)
    mean_pe = total_pe / len(results)
    mean_rank = total_rank / len(results)
    slack = mean_rank + 1 - 2 ** mean_pe
    conjecture_holds = slack <= 0
    counterexample = "" if conjecture_holds else f"Slack: {slack}"
    return {
        "metric_name": "Persistence Entropy",
        "metric_value": mean_pe,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    mean_pe = sum(result["metric_value"] for result in [run_trial(seed) for seed in seeds]) / len(seeds)
    slack = min(result["metric_value"] * -1 + 1 - 2 ** result["metric_value"] for result in [run_trial(seed) for seed in seeds])
    support_fraction = sum(1 for result in [run_trial(seed) for seed in seeds] if result["conjecture_holds"]) / len(seeds)
    if slack <= 0:
        print(f"RESULT: SUPPORTED mean={mean_pe} std=NA support_fraction={support_fraction}")
    else:
        print(f"RESULT: FALSIFIED counterexample='Slack: {slack}' first_failing_seed={seeds[slack > 0]}")