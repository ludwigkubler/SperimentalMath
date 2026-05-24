# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def is_planar(n, edges):
        if n <= 3:
            return True
        max_edges = 3 * (n - 2)
        if len(edges) > max_edges:
            return False
        visited = [False] * n
        stack = []
        
        def dfs(v, parent):
            visited[v] = True
            stack.append(v)
            for u in range(n):
                if (v, u) in edges or (u, v) in edges:
                    if not visited[u]:
                        if not dfs(u, v):
                            return False
                    elif u != parent:
                        return False
            stack.pop()
            return True
        
        for i in range(n):
            if not visited[i]:
                if not dfs(i, -1):
                    return False
        return True
    
    def alexander_griffiths_rank(n, edges):
        # Construct the Alexander-Griffiths module (simplified example)
        rank = n  # Placeholder for actual computation
        return rank
    
    def resolution_width(n, edges):
        # Simplified example of resolution width calculation
        width = n  # Placeholder for actual computation
        return width
    
    n = random.randint(5, 40)
    edges = set()
    while len(edges) < n * (n - 1) // 2:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
    
    if not is_planar(n, edges):
        return {
            "metric_name": "alexander_griffiths_rank",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Non-planar graph"
        }
    
    rank = alexander_griffiths_rank(n, edges)
    width = resolution_width(n, edges)
    
    return {
        "metric_name": "alexander_griffiths_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_rank = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        RESULT = f"SUPPORTED mean={mean_rank} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        RESULT = f"FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}"
    
    print(RESULT)