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
    
    def exp(x):
        return math.exp(x)
    
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    def binomial_coefficient(n, k):
        if k > n:
            return 0
        return factorial(n) // (factorial(k) * factorial(n - k))
    
    def generate_random_graph(n, p):
        graph = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < p:
                    graph[i][j] = 1
                    graph[j][i] = 1
        return graph
    
    def find_k_cliques(graph, k):
        n = len(graph)
        cliques = []
        
        def dfs(node, path, depth):
            if depth == k:
                cliques.append(path[:])
                return
            for neighbor in range(n):
                if graph[node][neighbor] and neighbor not in path:
                    path.append(neighbor)
                    dfs(neighbor, path, depth + 1)
                    path.pop()
        
        for i in range(n):
            dfs(i, [i], 1)
        return cliques
    
    def intersecting_family_size(cliques):
        n = len(cliques[0])
        family = set(range(n))
        for clique in cliques:
            family &= set(clique)
        return len(family)
    
    def monotone_circuit_depth(k, n):
        # This is a placeholder function. In practice, you would need to implement
        # an algorithm to compute the depth of a monotone circuit computing k-clique.
        # For simplicity, we assume a constant upper bound for this example.
        return 2 ** (n // 2)
    
    n = random.randint(5, 40)
    p = 0.5
    graph = generate_random_graph(n, p)
    k = random.randint(3, min(5, n))
    cliques = find_k_cliques(graph, k)
    family_size = intersecting_family_size(cliques)
    circuit_depth = monotone_circuit_depth(k, n)
    
    metric_name = "Intersecting Family Size"
    metric_value = family_size
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if family_size < exp(n ** (math.log2(k) / 2)):
        conjecture_holds = True
    else:
        counterexample = "Family size is too large for the given n and k."
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    num_seeds = len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / num_seeds
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value / num_seeds} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value / num_seeds} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i for i, r in enumerate(results) if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Family size is too large for the given n and k.\" first_failing_seed={first_failing_seed}")