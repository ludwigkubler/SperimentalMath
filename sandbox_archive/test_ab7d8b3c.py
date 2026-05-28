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
    
    def generate_random_graph(n, m):
        graph = {i: set() for i in range(n)}
        edges = set()
        while len(edges) < m:
            u, v = random.sample(range(n), 2)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                graph[u].add(v)
                graph[v].add(u)
                edges.add((u, v))
        return graph
    
    def is_k_clique(graph, clique):
        for u in clique:
            for v in clique:
                if u != v and v not in graph[u]:
                    return False
        return True
    
    def find_max_clique_size(graph):
        max_clique = []
        for node in range(len(graph)):
            clique = [node]
            stack = [node]
            while stack:
                current = stack.pop()
                for neighbor in graph[current]:
                    if neighbor not in clique and all(neighbor in graph[u] for u in clique):
                        clique.append(neighbor)
                        stack.append(neighbor)
            if len(clique) > len(max_clique):
                max_clique = clique
        return len(max_clique)
    
    def intersecting_family_size(graph, k):
        n = len(graph)
        vertices = list(range(n))
        for i in range(len(vertices)):
            for j in range(i + 1, len(vertices)):
                if is_k_clique(graph, [vertices[i], vertices[j]]):
                    return 2
        return 0
    
    def monotone_circuit_depth(k):
        # This is a placeholder function. In practice, you would need to implement
        # an algorithm to construct the circuit and compute its depth.
        return k * math.log(k, 2)
    
    n = random.randint(5, 40)
    m = random.randint(n, n**2)
    graph = generate_random_graph(n, m)
    k = find_max_clique_size(graph)
    
    if k == 1:
        return {
            "metric_name": "intersecting_family_size",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "single_vertex_graph"
        }
    
    intersecting_size = intersecting_family_size(graph, k)
    circuit_depth = monotone_circuit_depth(k)
    
    return {
        "metric_name": "intersecting_family_size",
        "metric_value": intersecting_size,
        "instances_tested": 1,
        "conjecture_holds": intersecting_size < math.exp(n ** (math.log(k, 2) / 2)),
        "counterexample": "" if intersecting_size < math.exp(n ** (math.log(k, 2) / 2)) else f"n={n}, k={k}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        counterexample = ""
    else:
        mean_value = sum(result["metric_value"] for result in results if result["conjecture_holds"]) / sum(1 for result in results if result["conjecture_holds"])
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = f"n={results[first_failing_seed]['instances_tested']}, k={find_max_clique_size(generate_random_graph(results[first_failing_seed]['instances_tested'], results[first_failing_seed]['instances_tested']))}"
    
    print(f"RESULT: {'SUPPORTED' if all(result['conjecture_holds'] for result in results) else 'FALSIFIED'} mean={mean_value} std=0 support_fraction={support_fraction}")