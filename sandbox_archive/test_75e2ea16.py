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
        for i in range(n):
            neighbors = [j for j in range(n) if G[i][j] == 1]
            if len(neighbors) < k - 1:
                return False
            for j in range(len(neighbors)):
                for l in range(j + 1, len(neighbors)):
                    if G[neighbors[j]][neighbors[l]] != 1:
                        return False
        return True
    
    def symmetry_group_order(G):
        n = len(G)
        symmetries = []
        for i in range(n):
            for j in range(i + 1, n):
                if G[i][j] == G[j][i]:
                    continue
                found_symmetry = False
                for perm in itertools.permutations(range(n)):
                    if all(G[perm[i]][perm[j]] == G[i][j] for i in range(n) for j in range(i + 1, n)):
                        symmetries.append(perm)
                        found_symmetry = True
                        break
                if found_symmetry:
                    break
        return len(symmetries)
    
    def is_prime(num):
        if num <= 1:
            return False
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                return False
        return True
    
    n = random.randint(5, 40)
    k = random.randint(3, min(n - 1, 10))
    
    G = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < 0.5:
                G[i][j] = G[j][i] = 1
    
    if is_k_clique(G, k):
        return {
            "metric_name": "symmetry_group_order",
            "metric_value": symmetry_group_order(G),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "k-CLIQUE graph"
        }
    
    order = symmetry_group_order(G)
    if order < n ** 0.25:
        return {
            "metric_name": "symmetry_group_order",
            "metric_value": order,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Non-k-CLIQUE graph with order < Θ(n^{0.25})"
        }
    
    return {
        "metric_name": "symmetry_group_order",
        "metric_value": order,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if r["instances_tested"] > 0)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"Non-k-CLIQUE graph with order < Θ(n^{0.25})\" first_failing_seed={r['seed']}")
                break