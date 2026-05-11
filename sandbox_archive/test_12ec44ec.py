# auto-injected by SEC sandbox
import math
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from collections import defaultdict

def generate_random_graph(n):
    graph = defaultdict(set)
    for i in range(n):
        for j in range(i + 1, n):
            if random.choice([True, False]):
                graph[i].add(j)
                graph[j].add(i)
    return graph

def tutte_polynomial(graph, memo=None):
    if memo is None:
        memo = {}
    if (graph,) in memo:
        return memo[(graph,)]
    
    n = len(graph)
    if n == 0:
        return 1
    if n == 1:
        return 2
    
    v = next(iter(graph))
    edges = [(v, u) for u in graph[v]]
    T = 0
    for e in edges:
        u, w = e
        G_uw = {u: set(), w: set()}
        for x in graph[u]:
            if x != w:
                G_uw[u].add(x)
        for y in graph[w]:
            if y != u:
                G_uw[w].add(y)
        for x in graph[u]:
            for y in graph[w]:
                if x != y and (x, y) not in edges:
                    G_uw[x].add(y)
        
        T += tutte_polynomial(G_uw, memo)
    
    memo[(graph,)] = T
    return T

def get_tutte_values(graph, k):
    T21 = tutte_polynomial(graph)
    T12 = tutte_polynomial({u: {v for v in graph[u] if v > u} for u in range(k)})
    return T21, T12

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_random_graph(n)
        T21, T12 = get_tutte_values(graph, n // 2 + 1)
        
        if T21 < n ** (n // 4) or T12 < n ** (n // 4):
            return {
                "metric_name": "T(2,1), T(1,2)",
                "metric_value": None,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": f"Failed for n={n}, T(2,1)={T21}, T(1,2)={T12}"
            }
        
        results.append(T21)
    
    return {
        "metric_name": "T(2,1), T(1,2)",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = (sum((x - mean) ** 2 for x in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r is not None and r >= n_values[-1] ** (n_values[-1] // 4)) / len(results)
    
    if all(r is not None and r >= n_values[-1] ** (n_values[-1] // 4) for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r is not None and r < n_values[-1] ** (n_values[-1] // 4) for r in results):
        first_failing_seed = seeds[results.index(next(r for r in results if r is not None and r < n_values[-1] ** (n_values[-1] // 4)))]
        print(f"RESULT: FALSIFIED counterexample='T(2,1), T(1,2) < n^{n_values[-1]//4}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")