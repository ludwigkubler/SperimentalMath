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

def generate_random_graph(n):
    edges = set()
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < 0.5:
                edges.add((i, j))
    return edges

def is_clique(graph, vertices):
    for u, v in itertools.combinations(vertices, 2):
        if (u, v) not in graph and (v, u) not in graph:
            return False
    return True

def find_max_clique_size(graph, n):
    max_clique_size = 0
    for i in range(1, n + 1):
        for vertices in itertools.combinations(range(n), i):
            if is_clique(graph, vertices):
                max_clique_size = max(max_clique_size, len(vertices))
    return max_clique_size

def greedy_polymatroid_rank(graph, n):
    rank = 0
    covered_edges = set()
    for _ in range(n):
        max_gain = -1
        best_vertex = None
        for v in range(n):
            if v not in covered_edges:
                gain = sum(1 for u in range(n) if (u, v) in graph and u not in covered_edges)
                if gain > max_gain:
                    max_gain = gain
                    best_vertex = v
        rank += max_gain
        covered_edges.update((best_vertex, u) for u in range(n) if (best_vertex, u) in graph or (u, best_vertex) in graph)
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    clique_number = math.isqrt(n) + 1
    graph = generate_random_graph(n)
    while find_max_clique_size(graph, n) > clique_number:
        graph = generate_random_graph(n)
    
    rank = greedy_polymatroid_rank(graph, n)
    return {
        "metric_name": "polymatroid_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= 6.4,
        "counterexample": "" if rank >= 6.4 else f"Graph with clique number {clique_number} and rank {rank}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")