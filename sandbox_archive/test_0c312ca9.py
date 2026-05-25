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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_k_clique_graph(n, k):
        if n < k:
            return None
        vertices = list(range(n))
        edges = []
        for i in range(k):
            for j in range(i + 1, k):
                edges.append((vertices[i], vertices[j]))
        for _ in range(k, n):
            u = random.choice(vertices)
            v = random.choice(vertices)
            if (u, v) not in edges and (v, u) not in edges:
                edges.append((u, v))
        return edges
    
    def is_connected(graph, n):
        visited = [False] * n
        stack = [0]
        while stack:
            node = stack.pop()
            if not visited[node]:
                visited[node] = True
                for neighbor in graph:
                    if neighbor[0] == node and not visited[neighbor[1]]:
                        stack.append(neighbor[1])
                    elif neighbor[1] == node and not visited[neighbor[0]]:
                        stack.append(neighbor[0])
        return all(visited)
    
    def find_automorphisms(graph, n):
        if not is_connected(graph, n):
            return 0
        automorphisms = set()
        for perm in itertools.permutations(range(n)):
            new_graph = [(perm[u], perm[v]) for u, v in graph]
            if sorted(new_graph) == sorted(graph):
                automorphisms.add(tuple(perm))
        return len(automorphisms)
    
    def min_rank(automorphisms):
        if not automorphisms:
            return 0
        n = len(automorphisms)
        adjacency_matrix = [[0] * n for _ in range(n)]
        for i, perm in enumerate(automorphisms):
            for j, p in enumerate(perm):
                adjacency_matrix[i][j] = adjacency_matrix[j][i] = (p == i)
        rank = 0
        for row in adjacency_matrix:
            if any(row):
                rank += 1
                for i in range(n):
                    if row[i]:
                        for j in range(i + 1, n):
                            if adjacency_matrix[j][i]:
                                adjacency_matrix[j][i] = False
        return rank
    
    results = []
    for n in [10, 20, 30, 40]:
        graph = generate_k_clique_graph(n, k=5)
        if graph is None:
            continue
        automorphisms = find_automorphisms(graph, n)
        rank = min_rank(automorphisms)
        results.append(rank)
    
    if not results:
        return {
            "metric_name": "min_rank",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean = sum(results) / len(results)
    std = (sum((x - mean) ** 2 for x in results) / len(results)) ** 0.5
    support_fraction = Fraction(sum(1 for r in results if r <= 3 * n), len(results))
    
    return {
        "metric_name": "min_rank",
        "metric_value": mean,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= Fraction(8, 10),
        "counterexample": "" if support_fraction >= Fraction(8, 10) else f"mean={mean}, std={std}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        if not result["conjecture_holds"]:
            break
        results.append(result["metric_value"])
    
    if len(results) == len(seeds):
        mean = sum(results) / len(results)
        std = (sum((x - mean) ** 2 for x in results) / len(results)) ** 0.5
        support_fraction = Fraction(len(results), len(seeds))
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif result["counterexample"]:
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=30")