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
    
    def generate_graph(n):
        G = {i: [] for i in range(n)}
        edges = set()
        while len(edges) < n * (n - 1) // 2:
            u, v = sorted(random.sample(range(n), 2))
            if u != v and (u, v) not in edges and (v, u) not in edges:
                G[u].append(v)
                G[v].append(u)
                edges.add((u, v))
        return G
    
    def communication_complexity_rank(G):
        n = len(G)
        rank = 0
        visited = [False] * n
        for i in range(n):
            if not visited[i]:
                stack = [i]
                while stack:
                    u = stack.pop()
                    if not visited[u]:
                        visited[u] = True
                        rank += 1
                        stack.extend(v for v in G[u] if not visited[v])
        return rank
    
    def eta_invariant(G):
        n = len(G)
        orbit_space = set()
        for i in range(n):
            orbit_space.add(tuple(sorted(G[i])))
        return len(orbit_space)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        G = generate_graph(n)
        r_G = communication_complexity_rank(G)
        eta_G = eta_invariant(G)
        
        if eta_G > 0 and r_G > 0:
            instance_result = {
                "metric_name": "eta_invariant",
                "metric_value": eta_G,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": eta_G <= r_G**2,
                "counterexample": ""
            }
        else:
            instance_result = {
                "metric_name": "eta_invariant",
                "metric_value": None,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        results.append(instance_result)
    
    if any(not res["conjecture_holds"] for res in results):
        first_failing_seed = seed
        counterexample = f"eta(G)={results[0]['metric_value']}, r(G)^2={results[1]['metric_value']}"
        return {
            "seed": seed,
            "metric_name": "eta_invariant",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(res["n_max"] for res in results),
            "conjecture_holds": False,
            "counterexample": counterexample
        }
    else:
        return {
            "seed": seed,
            "metric_name": "eta_invariant",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(res["n_max"] for res in results),
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(res["conjecture_holds"] for res in results):
        mean_value = sum(res["metric_value"] for res in results) / len(results)
        std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        counterexample = f"eta(G)={results[0]['metric_value']}, r(G)^2={results[1]['metric_value']}"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")