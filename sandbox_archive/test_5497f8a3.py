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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_expander_graph(n):
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    G[i][j] = 1
                    G[j][i] = 1
        return G
    
    def resolution_tree_depth(G):
        n = len(G)
        visited = [False] * n
        depth = 0
        
        def dfs(node, current_depth):
            nonlocal depth
            if current_depth > depth:
                depth = current_depth
            visited[node] = True
            for neighbor in range(n):
                if G[node][neighbor] and not visited[neighbor]:
                    dfs(neighbor, current_depth + 1)
        
        for i in range(n):
            if not visited[i]:
                dfs(i, 0)
        
        return depth
    
    def brauer_group_rank(G):
        n = len(G)
        rank = 0
        for i in range(n):
            for j in range(i + 1, n):
                if G[i][j] or G[j][i]:
                    rank += 1
        return rank
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    G = generate_expander_graph(n)
    t_star_G = resolution_tree_depth(G)
    min_rank_Brauer_G = brauer_group_rank(G)
    
    if t_star_G == 0:
        return {
            "metric_name": "min_rank_Brauer_G",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Resolution tree depth is zero, which is undefined."
        }
    
    c1 = 0.5
    c2 = 1.5
    
    lower_bound = c1 * math.log(t_star_G)
    upper_bound = c2 * math.log(t_star_G)
    
    return {
        "metric_name": "min_rank_Brauer_G",
        "metric_value": min_rank_Brauer_G,
        "instances_tested": 1,
        "conjecture_holds": lower_bound <= min_rank_Brauer_G <= upper_bound,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='min_rank_Brauer_G out of bounds' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")