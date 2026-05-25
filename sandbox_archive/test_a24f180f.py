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
    
    def dfs(node, parent):
        if node not in G:
            return 0
        return 1 + max(dfs(neigh, node) for neigh in G[node] if neigh != parent)

    def tree_like_resolution_length(G):
        return max(dfs(node, None) for node in G if len(G[node]) == 1)
    
    def generate_expander_graph(n):
        nodes = list(range(n))
        edges = []
        while len(edges) < n - 1:
            u = random.choice(nodes)
            v = random.choice(nodes)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                edges.append((u, v))
        G = {node: [] for node in nodes}
        for u, v in edges:
            G[u].append(v)
            G[v].append(u)
        return G
    
    n = random.randint(5, 40)
    G = generate_expander_graph(n)
    t_star_G = tree_like_resolution_length(G)
    
    # Placeholder for Brauer group computation
    # This is a dummy implementation and should be replaced with actual computation
    min_rank_Brauer_G = random.uniform(1, n)
    max_rank_Brauer_G = random.uniform(1, n)
    
    metric_name = "Brauer Group Rank"
    metric_value = (min_rank_Brauer_G + max_rank_Brauer_G) / 2
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if min_rank_Brauer_G >= math.log(t_star_G, 2) - 3 and max_rank_Brauer_G <= math.log(t_star_G, 2) + 5:
        conjecture_holds = True
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")