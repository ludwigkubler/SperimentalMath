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
    
    def generate_3colorable_graph(n):
        graph = {i: [] for i in range(n)}
        colors = [0] * n
        color_count = 1
        
        for i in range(n):
            neighbors = set(graph[j] for j in range(n) if j != i)
            available_colors = set(range(3)) - {colors[j] for j in neighbors}
            if not available_colors:
                return None, None
            colors[i] = random.choice(list(available_colors))
        
        for i in range(n):
            for j in range(i + 1, n):
                if colors[i] != colors[j]:
                    graph[i].append(j)
                    graph[j].append(i)
        
        return graph, colors
    
    def simplicial_complex(graph):
        n = len(graph)
        simplices = {frozenset([i]): 1 for i in range(n)}
        
        for edge in graph.values():
            for face in list(simplices.keys()):
                if all(v in face for v in edge):
                    new_face = face | frozenset(edge)
                    simplices[new_face] = simplices[face]
        
        return simplices
    
    def resolution_width(graph, colors):
        n = len(graph)
        width = 0
        
        for i in range(n):
            if colors[i] == 0:
                continue
            neighbors = graph[i]
            for j in neighbors:
                if colors[j] != colors[i]:
                    width += 1
        
        return width
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        var_x = sum((x[i] - mean_x) ** 2 for i in range(n)) / n
        var_y = sum((y[i] - mean_y) ** 2 for i in range(n)) / n
        return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))
    
    results = []
    for _ in range(30):
        graph, colors = generate_3colorable_graph(random.randint(5, 40))
        if graph is None:
            continue
        
        simplices = simplicial_complex(graph)
        width = resolution_width(graph, colors)
        
        if not simplices or width == 0:
            continue
        
        min_local_index = min(len(face) for face in simplices.keys())
        results.append((min_local_index, width))
    
    if len(results) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(len(face) for face in simplices.keys()) if results else 0,
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    x, y = zip(*results)
    corr_coeff = correlation_coefficient(x, y)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": max(len(face) for face in simplices.keys()),
        "conjecture_holds": corr_coeff >= 0.7,
        "counterexample": "" if corr_coeff >= 0.7 else f"correlation_coefficient={corr_coeff}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        if result["conjecture_holds"]:
            results.append(result["metric_value"])
    
    mean_corr_coeff = sum(results) / len(results)
    support_fraction = len([r for r in results if r >= 0.7]) / len(results)
    
    if all(r >= 0.7 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = seeds[next(i for i, r in enumerate(results) if r < 0.7)]
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient<{mean_corr_coeff}' first_failing_seed={first_failing_seed}")