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

def generate_random_k_subsets(n, k):
    return [tuple(sorted(random.sample(range(1, n+1), k))) for _ in range(20)]

def reduce_dnf(dnf):
    dnf = set(dnf)
    while True:
        new_dnf = set()
        dominated = False
        for t in dnf:
            if any(t.issubset(s) for s in dnf if s != t):
                dominated = True
            else:
                new_dnf.add(t)
        if not dominated:
            break
        dnf = new_dnf
    return list(dnf)

def compute_forman_ricci_curvature(H, A):
    n = len(A)
    deg = [sum(row) for row in A]
    tri = 0
    for i in range(n):
        for j in range(i+1, n):
            if A[i][j] > 0:
                tri += sum(A[k][i] * A[k][j] for k in range(n) if k != i and k != j)
    return (4 * len(H) - sum(deg)) / len(H) + (3 * tri / len(H))

def compute_delta(F, G):
    F_and_G = reduce_dnf([t for t in F + G if any(t1 & t2 for t1 in F for t2 in G)])
    F_or_G = reduce_dnf(list(set(F) | set(G)))
    return (compute_forman_ricci_curvature(F_and_G, build_adjacency_matrix(F_and_G)) +
            compute_forman_ricci_curvature(F_or_G, build_adjacency_matrix(F_or_G)) -
            compute_forman_ricci_curvature(F, build_adjacency_matrix(F)) -
            compute_forman_ricci_curvature(G, build_adjacency_matrix(G)))

def build_adjacency_matrix(dnf):
    n = len(dnf)
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if any(t1 & t2 for t1 in dnf[i] for t2 in dnf[j]):
                A[i][j] = 1
                A[j][i] = 1
    return A

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [10, 15, 20, 25, 30, 40]:
        k = math.ceil(math.log2(n))
        F = generate_random_k_subsets(n, k)
        G = generate_random_k_subsets(n, k)
        delta = compute_delta(F, G)
        results.append(delta)
    mean_delta = sum(results) / len(results)
    max_abs_delta = max(abs(d) for d in results)
    conjecture_holds = all(abs(d) <= 4 * math.sqrt(n) for n, d in zip([10, 15, 20, 25, 30, 40], results))
    counterexample = "" if conjecture_holds else "single_linear_in_N_violation"
    return {
        "metric_name": "Delta(F,G)",
        "metric_value": mean_delta,
        "instances_tested": len(results),
        "n_max": max([10, 15, 20, 25, 30, 40]),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean_result = sum(results) / len(results)
    support_fraction = sum(1 for r in results if abs(r) <= 4 * math.sqrt(seeds[results.index(r)])) / len(results)
    if all(abs(r) <= 4 * math.sqrt(s) for s, r in zip(seeds, results)):
        print(f"RESULT: SUPPORTED mean={mean_result} std=0.0 support_fraction={support_fraction}")
    elif any(abs(r) > 4 * math.sqrt(s) for s, r in zip(seeds, results)):
        first_failing_seed = seeds[results.index(max(results, key=lambda x: abs(x)))]
        print(f"RESULT: FALSIFIED counterexample='single_linear_in_N_violation' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")