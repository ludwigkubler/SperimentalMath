# auto-injected by SEC sandbox
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
import math
from collections import defaultdict

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def bfs(graph, start):
        queue = [start]
        visited = set(queue)
        distance = {start: 0}
        while queue:
            node = queue.pop(0)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    distance[neighbor] = distance[node] + 1
        return max(distance.values())
    
    def is_monotone(f):
        n = len(f)
        for i in range(n):
            for j in range(i+1, n):
                if f[i] and not f[j]:
                    return False
        return True
    
    def monotone_kw_depth(f):
        n = len(f)
        memo = {}
        
        def minimax(node, depth=0):
            if node in memo:
                return memo[node]
            if all(f[i] for i in range(n)):
                return depth
            min_val = float('inf')
            for i in range(n):
                if not f[i]:
                    continue
                new_f = list(f)
                new_f[i] = False
                min_val = min(min_val, minimax(tuple(new_f), depth + 1))
            memo[node] = min_val
            return min_val
        
        return minimax(tuple(f))
    
    def token_sliding_diameter(B):
        minterms, maxterms = B
        graph = defaultdict(list)
        for m in minterms:
            for i in range(len(m)):
                if not m[i]:
                    continue
                new_m = list(m)
                new_m[i] = False
                for j in range(len(maxterms)):
                    if all(new_m[k] == maxterms[j][k] for k in range(len(m))):
                        graph[(m, i)].append((maxterms[j], i))
        return bfs(graph, ((tuple([False]*len(minterms)), 0), (tuple([True]*len(maxterms)), 0)))
    
    def generate_monotone_function(n):
        minterms = list(itertools.product([False, True], repeat=n))
        maxterms = [not x for x in minterms]
        return random.choice(minterms)
    
    n = random.randint(3, 8)
    f = generate_monotone_function(n)
    B = ([tuple(f)], [tuple(not f[i] for i in range(n))])
    D_TS = token_sliding_diameter(B)
    D_m = monotone_kw_depth(f)
    
    if not is_monotone(f):
        return {
            "metric_name": "D_m(f)",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    metric_value = D_m
    conjecture_holds = D_m >= math.log2(D_TS + 1) - 1
    
    return {
        "metric_name": "D_m(f)",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Counterexample for n={n}, D_m(f)={D_m}, log2(D_TS+1)-1={math.log2(D_TS + 1) - 1}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values)/len(metric_values))} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")