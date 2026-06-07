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
    
    def is_planar(n, edges):
        if n < 3:
            return True
        if len(edges) > 3 * (n - 2):
            return False
        graph = [[] for _ in range(n)]
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
        
        def dfs(node, parent, visited):
            visited[node] = True
            stack = [(node, parent)]
            while stack:
                current, prev = stack.pop()
                for neighbor in graph[current]:
                    if not visited[neighbor]:
                        stack.append((neighbor, current))
                    elif neighbor != prev:
                        return False
            return True
        
        def is_bipartite(node, color_map):
            color_map[node] = 0
            queue = [node]
            while queue:
                u = queue.pop(0)
                for v in graph[u]:
                    if v not in color_map:
                        color_map[v] = 1 - color_map[u]
                        queue.append(v)
                    elif color_map[v] == color_map[u]:
                        return False
            return True
        
        def is_connected():
            visited = [False] * n
            for i in range(n):
                if not visited[i]:
                    dfs(i, -1, visited)
                    break
            return all(visited)
        
        if not is_connected():
            return {"metric_name": "h_min", "metric_value": 0, "instances_tested": 1, "n_max": n, "conjecture_holds": False, "counterexample": "not_planar"}
        
        if not is_bipartite(0, {}):
            return {"metric_name": "h_min", "metric_value": 0, "instances_tested": 1, "n_max": n, "conjecture_holds": False, "counterexample": "not_bipartite"}
        
        h_min = len(edges) - (n - 2)
        return {"metric_name": "h_min", "metric_value": h_min, "instances_tested": 1, "n_max": n, "conjecture_holds": True, "counterexample": ""}

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}")
    else:
        print(f"RESULT: FALSIFIED counterexample=\"not_planar\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}")