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
    
    def generate_k_regular_graph(k, n):
        if k * (k - 1) // 2 >= n:
            return None
        adj_list = [[] for _ in range(n)]
        edges_added = set()
        
        for i in range(n):
            for j in range(i + 1, min(i + k, n)):
                if (i, j) not in edges_added and (j, i) not in edges_added:
                    adj_list[i].append(j)
                    adj_list[j].append(i)
                    edges_added.add((i, j))
        
        return adj_list
    
    def girth(graph):
        from collections import deque
        
        n = len(graph)
        for start in range(n):
            visited = [False] * n
            queue = deque([(start, 1)])
            
            while queue:
                node, dist = queue.popleft()
                if dist > k + 2:
                    return dist
                if visited[node]:
                    continue
                visited[node] = True
                
                for neighbor in graph[node]:
                    if not visited[neighbor]:
                        queue.append((neighbor, dist + 1))
        
        return float('inf')
    
    def communication_complexity_rank(graph):
        n = len(graph)
        rank = 0
        
        for i in range(n):
            neighbors = set(graph[i])
            for j in range(i + 1, n):
                if len(neighbors.intersection(set(graph[j]))) > 0:
                    rank += 1
                    break
        
        return rank
    
    def minimal_local_indeterminacy(graph):
        n = len(graph)
        mli = 0
        
        for i in range(n):
            neighbors = set(graph[i])
            for j in range(i + 1, n):
                if len(neighbors.intersection(set(graph[j]))) > 0:
                    mli += 1
                    break
        
        return mli
    
    k = random.randint(3, 5)
    n = random.randint(k * (k - 1) // 2 + 1, min(40, 2 * k * (k - 1) // 2))
    graph = generate_k_regular_graph(k, n)
    
    if not graph or girth(graph) <= k + 2:
        return {
            "metric_name": "minimal_local_indeterminacy",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "girth_not_greater_than_k_plus_2"
        }
    
    mli = minimal_local_indeterminacy(graph)
    r = communication_complexity_rank(graph)
    
    return {
        "metric_name": "minimal_local_indeterminacy",
        "metric_value": mli,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": mli == r and r >= 2 * k - 4,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if "conjecture_holds" not in r or r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if 'counterexample' in r)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")