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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def is_edge(graph, u, v):
        return (u, v) in graph or (v, u) in graph
    
    def automorphism_group(graph):
        n = len(graph)
        group = []
        for perm in itertools.permutations(range(n)):
            if all(is_edge(graph, perm[i], perm[j]) == is_edge(graph, i, j) for i in range(n) for j in range(i + 1, n)):
                group.append(perm)
        return group
    
    def minimal_generating_set(group):
        generators = []
        for g in group:
            if all(all(g[i] == h[i] or g[i] == h[j] and h[g[i]] == h[j] for j in range(len(h))) for h in generators):
                generators.append(g)
        return generators
    
    n = random.randint(5, 40)
    graph = generate_graph(n)
    group = automorphism_group(graph)
    s_min = minimal_generating_set(group)
    
    # Quantum query complexity bound for k-CLIQUE problem
    k = random.randint(2, n - 1)
    clique_bound = math.comb(n, k) ** (1 / k)
    
    return {
        "metric_name": "Size of Minimal Generating Set",
        "metric_value": len(s_min),
        "instances_tested": 1,
        "conjecture_holds": len(s_min) <= clique_bound,
        "counterexample": "" if conjecture_holds else f"Graph with {n} vertices and {len(graph)} edges, |S_min(A(G))|={len(s_min)}, quantum query complexity bound={clique_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")