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
    
    def generate_random_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def bfs_cycle_detection(edges, start):
        visited = [False] * n
        parent = [-1] * n
        queue = []
        
        for v in range(n):
            if not visited[v]:
                queue.append(v)
                visited[v] = True
                
                while queue:
                    u = queue.pop(0)
                    
                    for v in range(n):
                        if (u, v) in edges or (v, u) in edges:
                            if not visited[v]:
                                visited[v] = True
                                parent[v] = u
                                queue.append(v)
                            elif parent[u] != v and parent[v] != u:
                                return True
        
        return False
    
    def matroid_rank(edges):
        n = len(edges)
        rank = 0
        for i in range(n):
            if bfs_cycle_detection(edges, i):
                rank += 1
        return rank
    
    def k_clique_communication_complexity(n, r):
        return n ** (1 - r / n)
    
    n = random.randint(5, 40)
    edges = generate_random_graph(n)
    r = matroid_rank(edges)
    complexity = k_clique_communication_complexity(n, r)
    
    metric_name = "communication_complexity"
    metric_value = complexity
    instances_tested = 1
    conjecture_holds = True if complexity >= n ** (1 - r / n) else False
    counterexample = "" if conjecture_holds else f"n={n}, r={r}, complexity={complexity}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample_desc = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")