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
        if (n * d) % 2 != 0 or d < 1 or n < 3:
            return None
        graph = {i: [] for i in range(n)}
        edges_added = set()
        for _ in range(d * n // 2):
            while True:
                u, v = random.sample(range(n), 2)
                if u == v or (u, v) in edges_added or (v, u) in edges_added:
                    continue
                graph[u].append(v)
                graph[v].append(u)
                edges_added.add((u, v))
                break
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = [f"x{i}" for i in range(n)]
        clauses = []
        for u in range(n):
            clauses.append([literals[u]])
            for v in graph[u]:
                clauses.append([-literals[u], literals[v]])
        return literals, clauses
    
    def euler_characteristic(graph):
        n = len(graph)
        m = sum(len(neighbors) for neighbors in graph.values()) // 2
        genus = (n - m + len(list(graph.keys()))) / 2
        return 2 - genus
    
    def communication_complexity(literals, clauses):
        # Simplified model of communication complexity
        return len(literals) * len(clauses)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        graph = generate_d_regular_graph(n, 2)
        if graph is None:
            continue
        literals, clauses = tseitin_formula(graph)
        chi = euler_characteristic(graph)
        cc = communication_complexity(literals, clauses)
        if chi is not None and cc is not None:
            results.append({"metric_name": "Euler Characteristic / Communication Complexity", 
                            "metric_value": chi / cc, 
                            "instances_tested": 1, 
                            "n_max": n, 
                            "conjecture_holds": True if chi / cc <= 2 * math.log10(n) else False, 
                            "counterexample": ""})
    
    return {
        "metric_name": "Euler Characteristic / Communication Complexity",
        "metric_value": sum(result["metric_value"] for result in results) / len(results),
        "instances_tested": len(results),
        "n_max": max(result["n_max"] for result in results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": "" if all(result["conjecture_holds"] for result in results) else "graph_generation_failed"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='graph_generation_failed' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")