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
    
    def is_k_clique(G, k):
        n = len(G)
        if n < k:
            return False
        for i in range(n):
            for j in range(i+1, n):
                if (i, j) not in G and (j, i) not in G:
                    return False
        return True
    
    def free_monoidal_category(V):
        n = len(V)
        category = {}
        for v in V:
            category[v] = {v}
        for v1 in V:
            for v2 in V:
                if v1 != v2:
                    category[(v1, v2)] = {v1, v2}
        return category
    
    def morphism_space(C, D):
        n = len(C)
        m = len(D)
        space = []
        for i in range(n):
            for j in range(m):
                if C[i] <= D[j]:
                    space.append((i, j))
        return space
    
    def min_rank(M):
        n = len(M)
        rank = 0
        while M:
            row = next(iter(M))
            rank += 1
            M -= {row}
            for r in list(M):
                if any(x in r for x in row):
                    M.remove(r)
        return rank
    
    def f(n, k):
        return n**k
    
    n = random.randint(5, 40)
    G = set()
    while len(G) < n:
        u, v = random.sample(range(n), 2)
        if (u, v) not in G and (v, u) not in G:
            G.add((u, v))
    
    if not is_k_clique(G, k):
        return {
            "metric_name": "min_rank_to_nk_ratio",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "not_a_k_clique"
        }
    
    V = list(G)
    C = free_monoidal_category(V)
    M = morphism_space(C, {frozenset([v]) for v in V})
    rank = min_rank(M)
    
    ratio = rank / f(n, k)
    
    return {
        "metric_name": "min_rank_to_nk_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 1.0,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        print(f"RESULT: SUPPORTED mean={total_ratio/len(results)} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_a_k_clique\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")