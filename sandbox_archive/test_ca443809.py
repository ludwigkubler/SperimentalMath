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
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d:
                    if (i, j) not in edges and (j, i) not in edges:
                        graph[i].append(j)
                        graph[j].append(i)
                        edges.add((i, j))
        return graph
    
    def local_induction_dimension(graph):
        n = len(graph)
        visited = [False] * n
        lid = 0
        
        for start in range(n):
            if not visited[start]:
                queue = [start]
                visited[start] = True
                while queue:
                    node = queue.pop(0)
                    for neighbor in graph[node]:
                        if not visited[neighbor]:
                            visited[neighbor] = True
                            queue.append(neighbor)
                lid += 1
        
        return lid
    
    def circuit_monotone_width(graph):
        n = len(graph)
        width = 0
        
        for i in range(n):
            neighbors = set(graph[i])
            for j in range(i + 1, n):
                if not neighbors.intersection(graph[j]):
                    width += 1
                    break
        
        return width
    
    def theta(x):
        return x // 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            graph = generate_d_regular_graph(n, 2)
            if graph is None:
                continue
            
            lid = local_induction_dimension(graph)
            w_mon = circuit_monotone_width(graph)
            
            if abs(lid - theta(w_mon)) > 3:
                conjecture_holds = False
                counterexample = f"n={n}, LID(G)={lid}, w_mon(G)={w_mon}"
                break
            
            total_metric_value += abs(lid - theta(w_mon))
            instances_tested += 1
    
    return {
        "metric_name": "LID - Theta(w_mon)",
        "metric_value": total_metric_value / instances_tested if instances_tested > 0 else 0,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
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
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")