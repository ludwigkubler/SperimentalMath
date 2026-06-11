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
    
    def generate_random_graph(n):
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    G[i][j] = G[j][i] = 1
        return G
    
    def min_distance_separating_set(G):
        n = len(G)
        visited = [False] * n
        dist = [-1] * n
        queue = []
        
        for i in range(n):
            if not visited[i]:
                visited[i] = True
                dist[i] = 0
                queue.append(i)
                
                while queue:
                    u = queue.pop(0)
                    for v in range(n):
                        if G[u][v] and not visited[v]:
                            visited[v] = True
                            dist[v] = dist[u] + 1
                            queue.append(v)
        
        return max(dist) if any(d != -1 for d in dist) else -1
    
    def quotient_space_dimension(G, min_dist):
        n = len(G)
        quotient_set = set()
        
        for i in range(n):
            if G[i][i] == 0:
                continue
            for j in range(i + 1, n):
                if G[j][j] == 0 or (G[i][j] and dist[i] < dist[j]):
                    quotient_set.add(j)
        
        return len(quotient_set)
    
    def rank_variance(G):
        n = len(G)
        ranks = [sum(row) for row in G]
        mean_rank = sum(ranks) / n
        variance = sum((r - mean_rank) ** 2 for r in ranks) / n
        return variance
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        G = generate_random_graph(n)
        min_dist = min_distance_separating_set(G)
        if min_dist == -1:
            continue
        
        dim_quotient_space = quotient_space_dimension(G, min_dist)
        rank_var = rank_variance(G)
        
        results.append({
            "n": n,
            "dim_quotient_space": dim_quotient_space,
            "rank_var": rank_var
        })
    
    if not results:
        return {
            "metric_name": "dimension_of_quotient_space",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(r["n"] for r in results)
    instances_tested = len(results)
    dim_quotient_space_avg = sum(r["dim_quotient_space"] for r in results) / instances_tested
    rank_var_avg = sum(r["rank_var"] for r in results) / instances_tested
    
    if n_max < 16:
        return {
            "metric_name": "dimension_of_quotient_space",
            "metric_value": dim_quotient_space_avg,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max_too_small"
        }
    
    conjecture_holds = all(
        abs(dim_quotient_space_avg - math.sqrt(n)) / math.sqrt(n) <= 0.1
        and abs(rank_var_avg - (math.sqrt(n) * n)) / (math.sqrt(n) * n) <= 0.3
        for n in n_values
    )
    
    return {
        "metric_name": "dimension_of_quotient_space",
        "metric_value": dim_quotient_space_avg,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_trials_run")
        sys.exit(0)
    
    metric_values = [r["metric_value"] for r in results]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.4f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values)/len(metric_values)):.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")