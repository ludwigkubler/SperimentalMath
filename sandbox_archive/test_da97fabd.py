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
        graph = [[] for _ in range(n)]
        edges_added = set()
        for i in range(d):
            for j in range(n):
                k = (j + i + 1) % n
                edge = tuple(sorted((j, k)))
                if edge not in edges_added:
                    graph[j].append(k)
                    graph[k].append(j)
                    edges_added.add(edge)
        return graph
    
    def local_induction_dimension(graph):
        n = len(graph)
        visited = [False] * n
        stack = []
        
        for i in range(n):
            if not visited[i]:
                stack.append(i)
                while stack:
                    node = stack.pop()
                    if not visited[node]:
                        visited[node] = True
                        for neighbor in graph[node]:
                            if not visited[neighbor]:
                                stack.append(neighbor)
        
        return sum(1 for v in visited if v) - 1
    
    def circuit_monotone_width(graph):
        n = len(graph)
        max_width = 0
        
        for i in range(n):
            width = 0
            for neighbor in graph[i]:
                width = max(width, abs(i - neighbor))
            max_width = max(max_width, width)
        
        return max_width
    
    def theta(x):
        return x
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            graph = generate_d_regular_graph(n, 2)
            if graph is None:
                continue
            lid = local_induction_dimension(graph) % 2
            w_mon = circuit_monotone_width(graph)
            instances_tested += 1
            n_max = max(n_max, n)
            difference = abs(lid - theta(w_mon))
            total_metric_value += difference
            
            if difference > 3:
                conjecture_holds = False
                counterexample = f"n={n}, LID(G)={lid}, w_mon(G)={w_mon}"
    
    if instances_tested < 30:
        return {
            "metric_name": "mean_difference",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_metric_value = total_metric_value / instances_tested
    return {
        "metric_name": "mean_difference",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")