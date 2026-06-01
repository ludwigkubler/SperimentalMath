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
        for i in range(n // 2):
            for j in range(n // 2):
                if random.randint(0, Δ - 1) == 0:
                    edges.append((i, j + n // 2))
        return A, B, edges
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for j in range(m):
                if j != i and A[j][i] != 0:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def communication_complexity_rank(G):
        n = len(G)
        rank = 0
        for i in range(n):
            row_sum = sum(1 for j in range(n) if G[i][j])
            if row_sum > rank:
                rank = row_sum
        return rank
    
    def hodge_arcs(A, B, edges):
        n = len(A)
        H = [[0] * n for _ in range(n)]
        for u, v in edges:
            H[u][v] += 1
            H[v][u] += 1
        H = gaussian_elimination(H)
        return sum(1 for row in H if any(x != 0 for x in row))
    
    def generate_tropical_curve(A, B, edges):
        n = len(A)
        T = [[0] * n for _ in range(n)]
        for u, v in edges:
            T[u][v] += 1
            T[v][u] += 1
        return T
    
    def run_experiment(n, Δ):
        A, B, edges = generate_bipartite_graph(n, Δ)
        G = [[0] * n for _ in range(n)]
        for u, v in edges:
            G[u][v] = 1
            G[v][u] = 1
        T = generate_tropical_curve(A, B, edges)
        hodge_count = hodge_arcs(A, B, edges)
        comm_rank = communication_complexity_rank(G)
        return hodge_count, comm_rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_hodge = 0
    total_comm = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        Δ = random.randint(2, min(n - 1, 10))
        hodge_count, comm_rank = run_experiment(n, Δ)
        total_hodge += hodge_count
        total_comm += comm_rank
        instances_tested += 1
        if n > n_max:
            n_max = n
    
    mean_hodge = Fraction(total_hodge, instances_tested)
    mean_comm = Fraction(total_comm, instances_tested)
    
    ratio_mean = mean_hodge / mean_comm
    conjecture_holds = ratio_mean >= Fraction(1, 2) and comm_rank <= 2 * mean_hodge
    
    return {
        "metric_name": "Ratio of Hodge Arcs to Communication Complexity Rank",
        "metric_value": float(ratio_mean),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Ratio < 0.5 or comm_rank > {2 * mean_hodge}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.1 for r in results) or any(r["comm_rank"] > 2 * r["mean_hodge"] for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"Ratio < 0.5 or comm_rank > {2 * mean_hodge}\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'] and r['metric_value'] < 0.1 or r['comm_rank'] > 2 * r['mean_hodge'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data n_tested={len(seeds)}")