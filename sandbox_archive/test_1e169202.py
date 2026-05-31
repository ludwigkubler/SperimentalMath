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
        graph = {i: [] for i in range(n)}
        edges = set()
        for _ in range(d * n // 2):
            while True:
                u, v = random.sample(range(n), 2)
                if u == v or (u, v) in edges or (v, u) in edges:
                    continue
                graph[u].append(v)
                graph[v].append(u)
                edges.add((u, v))
                break
        return graph
    
    def euler_characteristic(graph):
        n = len(graph)
        m = sum(len(neighbors) for neighbors in graph.values()) // 2
        genus = (n - m + len(list(graph.keys()))) / 2
        return n - m + genus
    
    def communication_complexity(graph):
        n = len(graph)
        d = max(len(neighbors) for neighbors in graph.values())
        return n * math.log(d, 2)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        d = random.randint(2, min(n - 1, 4))
        graph = generate_d_regular_graph(n, d)
        if not graph:
            continue
        chi = euler_characteristic(graph)
        cc = communication_complexity(graph)
        results.append((chi, cc))
    
    if len(results) < 30:
        return {
            "metric_name": "Euler Characteristic / Communication Complexity",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _ in results),
            "conjecture_holds": False,
            "counterexample": "graph_generation_failed"
        }
    
    chi_sum = sum(chi for chi, cc in results)
    cc_sum = sum(cc for _, cc in results)
    mean_chi_over_cc = chi_sum / len(results) / cc_sum
    
    return {
        "metric_name": "Euler Characteristic / Communication Complexity",
        "metric_value": mean_chi_over_cc,
        "instances_tested": 30,
        "n_max": max(n for n, _ in results),
        "conjecture_holds": mean_chi_over_cc <= 2 * math.log10(max(n for n, _ in results)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "Euler Characteristic / Communication Complexity > 2 * log10(n)"
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(result['conjecture_holds'] for result in results) else 'FALSIFIED'} mean={mean_value} std={std_value} support_fraction={support_fraction}")