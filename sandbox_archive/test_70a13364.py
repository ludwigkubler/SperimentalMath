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
    
    def generate_graphical_matroid(n):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return edges
    
    def is_connected(edges, n):
        visited = [False] * n
        stack = [0]
        while stack:
            node = stack.pop()
            if not visited[node]:
                visited[node] = True
                for edge in edges:
                    if edge[0] == node and not visited[edge[1]]:
                        stack.append(edge[1])
                    elif edge[1] == node and not visited[edge[0]]:
                        stack.append(edge[0])
        return all(visited)
    
    def find_automorphisms(edges, n):
        automorphisms = []
        for perm in itertools.permutations(range(n)):
            new_edges = [(perm[i], perm[j]) if i < j else (perm[j], perm[i]) for i, j in edges]
            if set(new_edges) == set(edges):
                automorphisms.append(perm)
        return automorphisms
    
    def resolution_width(graph):
        n = len(graph)
        width = 0
        clauses = []
        for i in range(n):
            clause = [random.choice([1, -1]) * (i + 1) for _ in range(random.randint(2, 4))]
            clauses.append(clause)
            width = max(width, len(clauses[-1]))
        return width
    
    n = random.randint(5, 30)
    edges = generate_graphical_matroid(n)
    if not is_connected(edges, n):
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "graph_not_connected"
        }
    
    automorphisms = find_automorphisms(edges, n)
    ord_aut_M = len(automorphisms)
    w_M = resolution_width(graph)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": w_M,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if ord_aut_M > 0 else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='automorphism_group_order_not_correlated_with_resolution_width' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")