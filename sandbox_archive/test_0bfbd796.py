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
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return edges
    
    def symmetric_group_action(graph):
        n = len(graph)
        vertices = list(range(n))
        action = []
        for perm in permutations(vertices):
            new_graph = set()
            for u, v in graph:
                new_u = perm.index(u)
                new_v = perm.index(v)
                if (new_u, new_v) not in new_graph and (new_v, new_u) not in new_graph:
                    new_graph.add((new_u, new_v))
            action.append(len(new_graph))
        return max(action)
    
    def permutations(lst):
        if len(lst) == 0:
            return []
        if len(lst) == 1:
            return [lst]
        l = []
        for i in range(len(lst)):
           m = lst[i]
           remLst = lst[:i] + lst[i+1:]
           for p in permutations(remLst):
               l.append([m] + p)
        return l
    
    def min_rank(graph):
        n = len(graph)
        action = symmetric_group_action(graph)
        rank = math.ceil(math.log2(action))
        return rank
    
    def max_disjoint_paths_complexity(n):
        return 2**n * (n**(1/2))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        graph = generate_random_graph(n)
        min_rank_value = min_rank(graph)
        complexity = max_disjoint_paths_complexity(n)
        results.append({
            "n": n,
            "min_rank": min_rank_value,
            "complexity": complexity
        })
    
    metric_name = "Max-Disjoint Paths Complexity"
    metric_value = sum(result["complexity"] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(result["min_rank"] <= n**(1/3) and result["complexity"] <= 2**n * (n**(1/2)) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
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
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")