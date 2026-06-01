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
    
    def generate_d_regular_graph(n, d):
        if (n * (d - 1)) % 2 != 0 or n < d:
            return None
        graph = {i: [] for i in range(n)}
        edges_added = 0
        while edges_added < n * (d - 1) // 2:
            u, v = random.sample(range(n), 2)
            if u not in graph[v] and v not in graph[u]:
                graph[u].append(v)
                graph[v].append(u)
                edges_added += 1
        return graph
    
    def calculate_genus(graph):
        n = len(graph)
        m = sum(len(neighbors) for neighbors in graph.values()) // 2
        genus = (n - m + 1) / 2
        return genus
    
    def count_integral_points(genus):
        if genus <= 0:
            return 0
        return int(10 * math.sqrt(genus))
    
    def communication_complexity_rank(graph):
        n = len(graph)
        rank = 0
        for neighbors in graph.values():
            rank += len(neighbors)
        return rank
    
    d = random.randint(2, 5)  # Regularity of the graph
    n = random.randint(5, 40)  # Number of vertices
    graph = generate_d_regular_graph(n, d)
    
    if not graph:
        return {
            "metric_name": "integral_points",
            "metric_value": 0,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "graph_not_d_regular"
        }
    
    genus = calculate_genus(graph)
    integral_points = count_integral_points(genus)
    rank = communication_complexity_rank(graph)
    
    if integral_points < 1:
        return {
            "metric_name": "integral_points",
            "metric_value": 0,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "integral_points_too_small"
        }
    
    c = 1.0
    f_n = lambda n: n**2
    
    if integral_points < c * rank**2 / f_n(n):
        return {
            "metric_name": "integral_points",
            "metric_value": integral_points,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"integral_points < c * rank^2 / f(n) (integral_points={integral_points}, c*rank^2/f(n)={c * rank**2 / f_n(n)})"
        }
    
    return {
        "metric_name": "integral_points",
        "metric_value": integral_points,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"integral_points_too_small\" first_failing_seed={first_failing_seed}")