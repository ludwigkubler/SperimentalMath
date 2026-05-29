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
    
    def combinations(iterable, r):
        pool = list(iterable)
        n = len(pool)
        if r > n:
            return
        indices = list(range(r))
        yield tuple(pool[i] for i in indices)
        while True:
            for i in reversed(range(r)):
                if indices[i] != i + n - r:
                    break
            else:
                return
            indices[i] += 1
            for j in range(i+1, r):
                indices[j] = indices[j-1] + 1
            yield tuple(pool[i] for i in indices)
    
    def generate_clique_dnf(v, k):
        minterms = set()
        for S in combinations(range(v), k):
            minterm = frozenset(frozenset({i,j}) for i,j in combinations(S, 2))
            minterms.add(minterm)
        return minterms
    
    def forman_ricci_curvature(G):
        n = len(G)
        deg = [0] * n
        for u in range(n):
            for v in G[u]:
                deg[u] += 1
                deg[v] += 1
        total = 0
        for u in range(n):
            for v in G[u]:
                if deg[u] == 0 or deg[v] == 0:
                    continue
                total += (4 - deg[u] - deg[v])
        return Fraction(total, n * (n - 1))
    
    def generate_graph(minterms, k):
        n = len(minterms)
        G = [[] for _ in range(n)]
        edge_count = 0
        for i in range(n):
            for j in range(i + 1, n):
                if len(minterms[i].intersection(minterms[j])) == k - 1:
                    G[i].append(j)
                    G[j].append(i)
                    edge_count += 1
        return G, edge_count
    
    v_values = [4, 10, 16, 20]
    results = []
    
    for v in v_values:
        k = math.ceil(math.log2(v))
        F_v = generate_clique_dnf(v, k)
        minterms = list(F_v)
        n = len(minterms)
        
        if n < 30:
            return {
                "metric_name": "M(F*_v)",
                "metric_value": -1,
                "instances_tested": 0,
                "n_max": v,
                "conjecture_holds": False,
                "counterexample": "Too few instances"
            }
        
        for _ in range(30):
            perm = random.sample(range(v), v)
            minterms_permuted = [frozenset(frozenset((perm[i], perm[j])) for i, j in S) for S in F_v]
            G, edge_count = generate_graph(minterms_permuted, k)
            
            deg = [len(neighbors) for neighbors in G]
            curvature = forman_ricci_curvature(G)
            predicted_bound = 4 - 2 * k * (v - k)
            
            results.append({
                "metric_name": "M(F*_v)",
                "metric_value": len(F_v),
                "instances_tested": n,
                "n_max": v,
                "conjecture_holds": len(F_v) == math.comb(v, k) and abs(curvature - predicted_bound) <= 1,
                "counterexample": ""
            })
    
    return {
        "metric_name": "M(F*_v)",
        "metric_value": sum(r["metric_value"] for r in results),
        "instances_tested": len(results),
        "n_max": max(v_values),
        "conjecture_holds": all(r["conjecture_holds"] for r in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")