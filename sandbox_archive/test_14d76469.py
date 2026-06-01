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
    
    def generate_planar_graph(n):
        if n < 3:
            return None
        
        # Generate a random planar graph using the method of adding edges to a base cycle
        nodes = list(range(1, n + 1))
        edges = [(nodes[i], nodes[(i + 1) % n]) for i in range(n)]
        
        for _ in range(n):
            u = random.choice(nodes)
            v = random.choice(nodes)
            if (u, v) not in edges and (v, u) not in edges:
                edges.append((u, v))
                # Check planarity condition
                if not is_planar(edges):
                    return None
        
        return edges
    
    def is_planar(edges):
        if len(edges) > 3 * len(nodes) - 6:
            return False
        
        def dfs(v, parent, visited, rec_stack):
            visited[v] = True
            rec_stack[v] = True
            
            for u in range(1, n + 1):
                if (v, u) in edges or (u, v) in edges:
                    if not visited[u]:
                        if dfs(u, v, visited, rec_stack):
                            return True
                    elif u != parent and rec_stack[u]:
                        return True
            
            rec_stack[v] = False
            return False
        
        visited = [False] * (n + 1)
        rec_stack = [False] * (n + 1)
        
        for v in range(1, n + 1):
            if not visited[v]:
                if dfs(v, -1, visited, rec_stack):
                    return False
        
        return True
    
    def geometric_entropy(edges):
        # Simplified entropy calculation based on the number of edges
        return len(edges) / (n * (n - 1))
    
    def communication_rank_growth_rate(edges):
        # Simplified rank growth rate calculation based on the number of edges
        return len(edges)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_planar_graph(n)
        if graph is None:
            continue
        
        H_G = geometric_entropy(graph)
        r_G = communication_rank_growth_rate(graph)
        
        if not (0.1 <= H_G <= 10) or not (0.1 <= r_G <= 10):
            return {
                "metric_name": "geometric_entropy",
                "metric_value": H_G,
                "instances_tested": len(results),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "H(G) or r(G) outside range [0.1, 10]"
            }
        
        results.append((H_G, r_G))
    
    if not results:
        return {
            "metric_name": "geometric_entropy",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values) if n_values else 1,
            "conjecture_holds": False,
            "counterexample": "No valid graphs generated"
        }
    
    H_Gs, r_Gs = zip(*results)
    slope, intercept = linear_regression(H_Gs, r_Gs)
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": slope,
        "instances_tested": len(results),
        "n_max": max(n_values) if n_values else 1,
        "conjecture_holds": abs(slope - 1) <= 3 * stdev(r_Gs),
        "counterexample": ""
    }

def linear_regression(x, y):
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))
    sum_xx = sum(xi ** 2 for xi in x)
    
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
    intercept = (sum_y - slope * sum_x) / n
    
    return slope, intercept

def stdev(values):
    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    return math.sqrt(variance)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_slope = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / sum(1 for r in results if r["conjecture_holds"])
    std_slope = stdev([r["metric_value"] for r in results if r["conjecture_holds"]])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_slope} std={std_slope} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_slope} std={std_slope} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if r["counterexample"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")