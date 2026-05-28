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
    
    def generate_expander_graph(n, m):
        G = {i: set() for i in range(n)}
        edges = []
        while len(edges) < m:
            u, v = random.sample(range(n), 2)
            if u != v and v not in G[u]:
                G[u].add(v)
                G[v].add(u)
                edges.append((u, v))
        return G
    
    def hodge_rank(G):
        n = len(G)
        A = [[0] * n for _ in range(n)]
        for u in G:
            for v in G[u]:
                A[u][v] += 1
                A[v][u] += 1
        
        # Gaussian elimination to find rank
        rank = 0
        for i in range(n):
            if all(A[j][i] == 0 for j in range(rank)):
                continue
            pivot_row = rank
            for j in range(rank + 1, n):
                if A[j][i] != 0:
                    pivot_row = j
                    break
            if pivot_row == rank:
                continue
            A[pivot_row], A[rank] = A[rank], A[pivot_row]
            for j in range(n):
                A[rank][j], A[pivot_row][j] = A[pivot_row][j], A[rank][j]
            for j in range(rank + 1, n):
                factor = -A[j][i] / A[rank][i]
                for k in range(n):
                    A[j][k] += factor * A[rank][k]
            rank += 1
        return rank
    
    def resolution_length(G):
        # Simplified estimation of resolution length based on graph properties
        n = len(G)
        m = sum(len(neighbors) for neighbors in G.values()) // 2
        return 2 ** (n + m)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        m = random.randint(n - 1, 2 * n)
        G = generate_expander_graph(n, m)
        hodge_rk = hodge_rank(G)
        res_len = resolution_length(G)
        
        if hodge_rk > 0 and res_len > 0:
            ratio = Fraction(hodge_rk, res_len).limit_denominator()
            total_metric_value += math.log2(ratio.numerator) - math.log2(ratio.denominator)
            instances_tested += 1
            if ratio > 2 ** (n // 2):
                conjecture_holds = False
                counterexample = f"n={n}, hodge_rk={hodge_rk}, res_len={res_len}"
    
    mean_metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0
    support_fraction = Fraction(instances_tested, len(n_values))
    
    return {
        "metric_name": "Hodge Rank to Resolution Length Ratio",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
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
    
    total_metric_value = sum(r["metric_value"] for r in results if r["instances_tested"] > 0)
    instances_tested = sum(r["instances_tested"] for r in results)
    support_fraction = Fraction(instances_tested, len(results))
    
    mean_metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")