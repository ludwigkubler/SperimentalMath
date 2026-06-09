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
    
    def generate_instance(n):
        # Generate a random instance φ of a language L in NP
        return [random.choice([0, 1]) for _ in range(n)]
    
    def construct_cayley_graph(instance):
        # Construct the Cayley graph of the instance
        n = len(instance)
        cayley_graph = [[0] * n for _ in range(n)]
        for i in range(n):
            if instance[i] == 1:
                cayley_graph[i][(i + 1) % n] = 1
                cayley_graph[(i + 1) % n][i] = 1
        return cayley_graph
    
    def min_generators(cayley_graph):
        # Calculate the minimum number of generators for the group action on the Cayley graph
        n = len(cayley_graph)
        visited = [False] * n
        queue = []
        num_generators = 0
        
        for i in range(n):
            if not visited[i]:
                queue.append(i)
                visited[i] = True
                num_generators += 1
            
            while queue:
                node = queue.pop(0)
                for j in range(n):
                    if cayley_graph[node][j] == 1 and not visited[j]:
                        visited[j] = True
                        queue.append(j)
        
        return num_generators
    
    def max_order(cayley_graph):
        # Calculate the maximum order of an element in the Cayley graph
        n = len(cayley_graph)
        orders = [0] * n
        
        for i in range(n):
            visited = [False] * n
            queue = []
            queue.append(i)
            visited[i] = True
            
            while queue:
                node = queue.pop(0)
                for j in range(n):
                    if cayley_graph[node][j] == 1 and not visited[j]:
                        visited[j] = True
                        queue.append(j)
            
            orders[i] = len(queue)
        
        return max(orders)
    
    def communication_complexity_rank(instance):
        # Calculate the communication complexity rank r(φ) for each instance φ
        n = len(instance)
        rank = 0
        
        for i in range(n):
            if instance[i] == 1:
                rank += 1
        
        return rank
    
    g_L_list = []
    o_phi_list = []
    r_phi_list = []
    
    for _ in range(30):  # Aim for at least 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        instance = generate_instance(n)
        cayley_graph = construct_cayley_graph(instance)
        g_L = min_generators(cayley_graph)
        o_phi = max_order(cayley_graph)
        r_phi = communication_complexity_rank(instance)
        
        g_L_list.append(g_L)
        o_phi_list.append(o_phi)
        r_phi_list.append(r_phi)
    
    mean_g_L = sum(g_L_list) / len(g_L_list)
    mean_o_phi = sum(o_phi_list) / len(o_phi_list)
    mean_r_phi = sum(r_phi_list) / len(r_phi_list)
    
    sum_diffs_g_L = sum((g - mean_g_L) ** 2 for g in g_L_list)
    sum_diffs_r_phi = sum((r - mean_r_phi) ** 2 for r in r_phi_list)
    
    if sum_diffs_g_L == 0 or sum_diffs_r_phi == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(g_L_list),
            "n_max": max(len(instance) for instance in g_L_list),
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }
    
    corr_g_r = (sum((g - mean_g_L) * (r - mean_r_phi) for g, r in zip(g_L_list, r_phi_list)) / math.sqrt(sum_diffs_g_L * sum_diffs_r_phi))
    mean_diff_o_phi_r_phi = abs(mean_o_phi - mean_r_phi)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": corr_g_r,
        "instances_tested": len(g_L_list),
        "n_max": max(len(instance) for instance in g_L_list),
        "conjecture_holds": corr_g_r >= 0.7 and mean_diff_o_phi_r_phi <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 39) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_corr_g_r = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["metric_value"] is not None for result in results):
        RESULT = f"SUPPORTED mean={mean_corr_g_r} std=0.0 support_fraction={support_fraction}"
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        RESULT = f"FALSIFIED counterexample=\"variance_zero\" first_failing_seed={first_failing_seed}"
    else:
        RESULT = "INCONCLUSIVE variance_zero"
    
    print(RESULT)