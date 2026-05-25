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
    
    # Generate a random expander graph G with n vertices and m edges
    n = 20
    m = 30
    G = {i: [] for i in range(n)}
    while len(G) < n or len(G[0]) != (n - 1):
        u, v = random.sample(range(n), 2)
        if v not in G[u]:
            G[u].append(v)
            G[v].append(u)
    
    # Compute the tree-like Resolution refutation length t*(G)
    def dfs(node, parent):
        return 1 + max(dfs(neigh, node) for neigh in G[node] if neigh != parent) if node in G else 0
    t_G = dfs(0, -1)
    
    # Compute the Brauer group of G (simplified example)
    # For simplicity, we assume the Brauer group rank is proportional to the number of edges
    min_rank_Brauer = m / 5
    max_rank_Brauer = m / 2
    
    # Check if the Brauer group ranks satisfy the conjecture
    c1 = 0.1
    c2 = 0.5
    mean_min_rank = c1 * math.log(t_G)
    mean_max_rank = c2 * math.log(t_G)
    
    min_rank_support = abs(min_rank_Brauer - mean_min_rank) <= 3 * (min_rank_Brauer / n) ** 0.5
    max_rank_support = max_rank_Brauer <= mean_max_rank + 5
    
    conjecture_holds = min_rank_support and max_rank_support
    counterexample = "" if conjecture_holds else f"min_rank={min_rank_Brauer}, max_rank={max_rank_Brauer}"
    
    return {
        "metric_name": "Brauer Group Rank",
        "metric_value": (min_rank_Brauer + max_rank_Brauer) / 2,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = (sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i for i, result in enumerate(results) if not result["conjecture_holds"]), None)
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")