# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def powerset(s):
        return list(chain.from_iterable(combinations(s, r) for r in range(len(s)+1)))
    
    def configuration_space(graph):
        n = len(graph)
        subsets = powerset(range(n))
        config_space = set()
        for subset in subsets:
            config = 0
            for i in subset:
                config |= (1 << i)
            config_space.add(config)
        return len(config_space)
    
    def circuit_depth(graph):
        n = len(graph)
        if n == 1:
            return 1
        depth = 2
        while True:
            new_edges = set()
            for u, v in graph:
                if u in subset and v not in subset:
                    new_edges.add((u, v))
                elif u not in subset and v in subset:
                    new_edges.add((v, u))
            if not new_edges:
                break
            depth += 1
            graph = new_edges
        return depth
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    r_values = []
    d_values = []
    
    for n in n_values:
        graph = random_graph(n)
        r = configuration_space(graph)
        d = circuit_depth(graph)
        r_values.append(r)
        d_values.append(d)
    
    if len(r_values) < 30 or len(d_values) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(r_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    corr = correlation_coefficient(r_values, d_values)
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": corr,
        "instances_tested": len(r_values),
        "n_max": max(n_values),
        "conjecture_holds": corr >= 0.7,
        "counterexample": ""
    }

def random_graph(n):
    edges = []
    for i in range(n):
        for j in range(i+1, n):
            if random.choice([True, False]):
                edges.append((i, j))
    return edges

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_corr = sum(r["metric_value"] for r in results) / len(results)
        std_corr = math.sqrt(sum((r["metric_value"] - mean_corr) ** 2 for r in results) / len(results))
        support_fraction = Fraction(len([r for r in results if r["conjecture_holds"]]), len(results))
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = "first_failing_seed"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")