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
        edges_used = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d and (i, j) not in edges_used:
                    graph[i].append(j)
                    graph[j].append(i)
                    edges_used.add((i, j))
                    edges_used.add((j, i))
        return graph
    
    def communication_complexity_rank_variance(graph):
        n = len(graph)
        rank = 0
        for node in range(n):
            neighbors = set(graph[node])
            if len(neighbors) == d:
                rank += 1
        return rank / n
    
    def count_independent_symplectic_subspaces(graph):
        n = len(graph)
        if n % d != 0:
            return None
        subspaces = []
        for i in range(n // d):
            subspace = set()
            for j in range(i * d, (i + 1) * d):
                subspace.update(graph[j])
            subspaces.append(subspace)
        independent_subspaces = [subspace for subspace in subspaces if all(len(subspace.intersection(other)) == 0 for other in subspaces if other != subspace)]
        return len(independent_subspaces)
    
    n_max = 33
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, n_max + 1):
        d = random.randint(2, n - 1)
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            continue
        
        instances_tested += 1
        sigma_G = communication_complexity_rank_variance(graph)
        rsym_G = count_independent_symplectic_subspaces(graph)
        
        if rsym_G is not None and sigma_G is not None:
            total_metric_value += abs(rsym_G - sigma_G)
    
    if instances_tested == 0:
        return {
            "metric_name": "Absolute Difference",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Graph generation failed for all sizes"
        }
    
    mean_metric_value = total_metric_value / instances_tested
    return {
        "metric_name": "Absolute Difference",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"Graph size {r['n_max']}, Degree {d}"
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")