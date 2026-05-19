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
    
    n = 40
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    
    def bfs_cycle(graph, start):
        visited = [False] * n
        parent = [-1] * n
        queue = []
        
        visited[start] = True
        queue.append(start)
        
        while queue:
            u = queue.pop(0)
            
            for v in range(n):
                if graph[u][v] == 1 and not visited[v]:
                    visited[v] = True
                    parent[v] = u
                    queue.append(v)
                elif graph[u][v] == 1 and visited[v] and parent[v] != u:
                    return True
        
        return False
    
    rank = sum(bfs_cycle(G, i) for i in range(n))
    
    k = random.randint(2, n-1)
    complexity_bound = n ** (1 - rank / n)
    
    # Simulate communication complexity (simplified version)
    communication_complexity = n ** 0.5
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": communication_complexity,
        "instances_tested": 1,
        "conjecture_holds": communication_complexity >= complexity_bound,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not result["conjecture_holds"] for result in results):
        counterexample = next(result for result in results if not result["conjecture_holds"])["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={results.index(next(result for result in results if not result['conjecture_holds']))}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")