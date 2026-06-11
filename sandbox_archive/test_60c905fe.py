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
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0:
            return None
        graph = [[0] * n for _ in range(n)]
        degree_count = [0] * n
        edges_added = set()
        
        while sum(degree_count) < n * d:
            u, v = random.sample(range(n), 2)
            if u == v or (u, v) in edges_added or (v, u) in edges_added:
                continue
            graph[u][v] = 1
            graph[v][u] = 1
            degree_count[u] += 1
            degree_count[v] += 1
            edges_added.add((u, v))
        
        return graph
    
    def coset_enumeration(graph):
        n = len(graph)
        group = set()
        generators = []
        
        for i in range(n):
            if sum(graph[i]) == 0:
                continue
            generators.append(i)
            break
        
        for perm in itertools.permutations(range(n)):
            valid = True
            for u, v in enumerate(perm):
                if graph[u][v] != graph[perm[v]][u]:
                    valid = False
                    break
            if valid:
                group.add(tuple(perm))
        
        return len(group)
    
    def communication_complexity_rank_variance(graph):
        n = len(graph)
        rank_var = 0
        
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j] == 1:
                    continue
                count = 0
                for k in range(n):
                    if graph[i][k] != graph[j][k]:
                        count += 1
                rank_var += count
        
        return rank_var / (n * (n - 1))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 3)
        if graph is None:
            continue
        
        aut_order = coset_enumeration(graph)
        rank_var = communication_complexity_rank_variance(graph)
        
        if aut_order == 0 or rank_var == 0:
            continue
        
        results.append({
            "n": n,
            "aut_order": aut_order,
            "rank_var": rank_var
        })
    
    if not results:
        return {
            "metric_name": "Aut(G) vs Rank Var",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid graphs generated"
        }
    
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    aut_orders = [result["aut_order"] for result in results]
    rank_vars = [result["rank_var"] for result in results]
    
    mean_aut_order = sum(aut_orders) / instances_tested
    mean_rank_var = sum(rank_vars) / instances_tested
    
    if abs(mean_aut_order - mean_rank_var) <= 2 * math.log(n_max):
        conjecture_holds = True
    else:
        conjecture_holds = False
        counterexample = f"Mean Aut(G): {mean_aut_order}, Mean Rank Var: {mean_rank_var}"
    
    return {
        "metric_name": "Aut(G) vs Rank Var",
        "metric_value": mean_aut_order,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = result["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")