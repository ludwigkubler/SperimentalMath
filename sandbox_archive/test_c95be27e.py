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
    
    def generate_expander_graph(n):
        # Generate a random expander graph with n nodes
        G = [[] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    G[i].append(j)
                    G[j].append(i)
        return G
    
    def resolution_tree_depth(G):
        # Compute the tree-like Resolution refutation length
        visited = [False] * len(G)
        depth = [0] * len(G)
        
        def dfs(node, current_depth):
            if visited[node]:
                return 0
            visited[node] = True
            max_child_depth = 0
            for neighbor in G[node]:
                child_depth = dfs(neighbor, current_depth + 1)
                if child_depth > max_child_depth:
                    max_child_depth = child_depth
            depth[node] = max_child_depth
            return max_child_depth
        
        dfs(0, 0)
        return max(depth)
    
    def brauer_group_rank(G):
        # Compute the rank of the Brauer group (simplified for testing)
        n = len(G)
        if n == 1:
            return 1
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
            "metric_name": "min_rank(Brauer(G))",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "t_star_G is zero"
        }
    
    c1 = 0.5
    c2 = 1.0
    expected_min_rank = c1 * math.log(t_star_G)
    expected_max_rank = c2 * math.log(t_star_G)
    
    return {
        "metric_name": "min_rank(Brauer(G))",
        "metric_value": min_rank_Brauer_G,
        "instances_tested": 1,
        "conjecture_holds": expected_min_rank <= min_rank_Brauer_G <= expected_max_rank and max_rank_Brauer_G <= expected_max_rank + 5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(3, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "min_rank(Brauer(G)) out of bounds"
        mean_metric_value = None
        std_metric_value = None
        support_fraction = 0.0
    
    print(f"RESULT: {'SUPPORTED' if all(r['conjecture_holds'] for r in results) else 'FALSIFIED'} mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")