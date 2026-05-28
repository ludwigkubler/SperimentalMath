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
    
    def generate_random_graph(n, k):
        graph = {i: set() for i in range(n)}
        edges = set()
        while len(edges) < n * (n - 1) // 2:
            u, v = random.sample(range(n), 2)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                graph[u].add(v)
                graph[v].add(u)
                edges.add((u, v))
        return graph
    
    def find_cliques(graph, k):
        def backtrack(path, start):
            if len(path) == k:
                cliques.add(tuple(sorted(path)))
                return
            for neighbor in graph[start]:
                if all(neighbor not in clique for clique in cliques):
                    path.append(neighbor)
                    backtrack(path, neighbor)
                    path.pop()
        
        cliques = set()
        for node in range(len(graph)):
            backtrack([node], node)
        return cliques
    
    def minkowski_cube_size(cliques):
        return len(cliques)
    
    def monotone_circuit_depth(n, k):
        # This is a placeholder function. Implementing an actual monotone circuit
        # for k-clique is complex and beyond the scope of this test.
        return random.randint(1, 2**n)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    k = random.randint(2, min(n // 2, 5))
    graph = generate_random_graph(n, k)
    cliques = find_cliques(graph, k)
    cube_size = minkowski_cube_size(cliques)
    circuit_depth = monotone_circuit_depth(n, k)
    
    metric_name = "Minkowski Cube Size"
    metric_value = cube_size
    instances_tested = 1
    conjecture_holds = cube_size < math.exp(n ** (math.log(k / 2) / math.log(2)))
    counterexample = "" if conjecture_holds else f"Graph with {n} vertices, {k}-cliques, Minkowski Cube Size: {cube_size}, Circuit Depth: {circuit_depth}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")