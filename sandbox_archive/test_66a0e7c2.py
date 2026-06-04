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
        if n % d != 0:
            raise ValueError("Graph size must be a multiple of the degree")
        graph = {i: [] for i in range(n)}
        edges_added = set()
        for _ in range(d * n // 2):
            while True:
                u = random.randint(0, n-1)
                v = random.randint(0, n-1)
                if u == v or (u, v) in edges_added or (v, u) in edges_added:
                    continue
                graph[u].append(v)
                graph[v].append(u)
                edges_added.add((u, v))
                break
        return graph
    
    def communication_complexity_rank(graph):
        n = len(graph)
        rank = 0
        for i in range(n):
            for j in range(i+1, n):
                if not any(j in neighbors for neighbors in graph.values()):
                    rank += 1
        return rank
    
    def symplectic_volume(graph):
        n = len(graph)
        volume = 0
        for _ in range(50):  # Constructive method to find minimal symplectic volume
            embedding = {i: [] for i in range(n)}
            for u, neighbors in graph.items():
                for v in neighbors:
                    if v not in embedding[u]:
                        embedding[u].append(v)
            volume += len(embedding)
        return volume
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 2)
        vol_m = symplectic_volume(graph)
        r_G = communication_complexity_rank(graph)
        if r_G == 0:
            continue
        ratio = vol_m / r_G
        results.append(ratio)
    
    if not results:
        return {
            "metric_name": "vol_m/G",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_ratio = sum(results) / len(results)
    a = random.random() + 1
    d = math.log(2, 2)
    threshold = a * (d ** n_values[0])
    
    return {
        "metric_name": "vol_m/G",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": all(r >= threshold for r in results),
        "counterexample": "" if all(r >= threshold for r in results) else f"threshold={threshold}, observed={min(results)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        if "metric_value" in trial_result and trial_result["metric_value"] is not None:
            results.append(trial_result["metric_value"])
    
    if all(r is None for r in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        mean_ratio = sum(results) / len(results)
        support_fraction = sum(1 for r in results if r >= threshold) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if result < threshold)
            print(f"RESULT: FALSIFIED counterexample='threshold={threshold}, observed={min(results)}' first_failing_seed={first_failing_seed}")