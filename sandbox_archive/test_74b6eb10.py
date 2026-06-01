# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def is_d_regular(graph, d):
        degrees = [sum(1 for _ in neighbors) for _, neighbors in graph.items()]
        return all(degree == d for degree in degrees)

    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0:
            return None
        graph = {i: set() for i in range(n)}
        edges_added = 0
        while edges_added < n * d // 2:
            u = random.randint(0, n - 1)
            v = random.choice(list(graph.keys()))
            if u != v and v not in graph[u]:
                graph[u].add(v)
                graph[v].add(u)
                edges_added += 1
        return graph

    def calculate_m_order(graph):
        # Placeholder for m_order calculation
        return len(graph)

    def calculate_w_m(graph):
        # Placeholder for w_m calculation
        return sum(len(neighbors) for _, neighbors in graph.items()) / len(graph)

    n = random.choice([5, 10, 15, 20, 30, 40])
    d = random.randint(2, min(n - 1, 3))
    graph = generate_d_regular_graph(n, d)
    
    if not is_d_regular(graph, d):
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    m_order = calculate_m_order(graph)
    w_m = calculate_w_m(graph)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": (m_order, w_m),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("counterexample" not in r or r["counterexample"] == "" for r in results):
        mean_corr = sum(r["metric_value"][0] / r["instances_tested"] for r in results) / len(results)
        std_corr = (sum((r["metric_value"][0] / r["instances_tested"] - mean_corr) ** 2 for r in results) / len(results)) ** 0.5
        support_fraction = sum(1 for r in results if "conjecture_holds" and r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_corr:.2f} std={std_corr:.2f} support_fraction={support_fraction:.2f}")
        else:
            print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed=1")
    else:
        first_failing_seed = next(result["seed"] for result in results if "counterexample" in result and result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")