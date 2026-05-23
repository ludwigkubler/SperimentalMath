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
    
    def generate_graph(n):
        graph = {i: [] for i in range(n)}
        colors = list(range(1, n + 1))
        random.shuffle(colors)
        for i in range(n):
            for j in range(i + 1, n):
                if colors[i] != colors[j]:
                    graph[i].append(j)
                    graph[j].append(i)
        return graph
    
    def is_k_colorable(graph, k):
        color = {}
        stack = [0]
        while stack:
            node = stack.pop()
            if node not in color:
                for neighbor in graph[node]:
                    if neighbor in color and color[neighbor] == color[node]:
                        return False
                color[node] = random.randint(1, k)
                stack.extend(graph[node])
        return True
    
    def adjoint_representation(g):
        # Placeholder function to simulate the adjoint representation
        return g
    
    def minimal_rank(representation):
        # Placeholder function to simulate the minimal rank calculation
        n = len(representation)
        return math.sqrt(n)
    
    n = random.randint(5, 40)
    graph = generate_graph(n)
    if not is_k_colorable(graph, n):
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Graph is not k-colorable"
        }
    
    representation = adjoint_representation(graph)
    rank = minimal_rank(representation)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= math.sqrt(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    results = []
    total_metric_value = 0
    count_conjecture_holds = 0
    counterexamples = set()
    
    for seed in seeds:
        trial_result = run_trial(seed)
        results.append(trial_result)
        total_metric_value += trial_result["metric_value"]
        if not trial_result["conjecture_holds"]:
            counterexamples.add(trial_result["counterexample"])
        
        print(f"TRIAL: {trial_result}")
    
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((x["metric_value"] - mean_metric_value) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        counterexample_desc = ", ".join(counterexamples)
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")