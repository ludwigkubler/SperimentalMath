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
        if (d * n) % 2 != 0 or d > n - 1:
            return None
        graph = {i: [] for i in range(n)}
        edges_added = set()
        for _ in range(d * n // 2):
            while True:
                u, v = random.sample(range(n), 2)
                if u != v and (u, v) not in edges_added and (v, u) not in edges_added:
                    graph[u].append(v)
                    graph[v].append(u)
                    edges_added.add((u, v))
                    break
        return graph

    def frege_proof_width(graph):
        n = len(graph)
        visited = [False] * n
        stack = []
        
        def dfs(node):
            if visited[node]:
                return 0
            visited[node] = True
            max_width = 1
            for neighbor in graph[node]:
                width = dfs(neighbor) + 1
                if width > max_width:
                    max_width = width
            stack.append(max_width)
            return max_width
        
        for node in range(n):
            if not visited[node]:
                dfs(node)
        
        return sum(stack)

    def p_adic_valuation_rank(graph):
        n = len(graph)
        valuations = [0] * n
        
        def p_adic_expansion(x, p):
            if x == 0:
                return 0
            count = 0
            while x % p == 0:
                x //= p
                count += 1
            return count
        
        for node in range(n):
            valuations[node] = sum(p_adic_expansion(len(graph[node]), i) for i in range(2, n))
        
        return max(valuations)

    def calculate_correlation_and_mean_difference(valranks, widths):
        if len(valranks) != len(widths):
            return 0, 0
        
        mean_valrank = sum(valranks) / len(valranks)
        mean_width = sum(widths) / len(widths)
        
        correlation = sum((valranks[i] - mean_valrank) * (widths[i] - mean_width) for i in range(len(valranks))) / (len(valranks) * math.sqrt(sum((valranks[i] - mean_valrank) ** 2 for i in range(len(valranks)))) * math.sqrt(sum((widths[i] - mean_width) ** 2 for i in range(len(widths)))))
        
        return correlation, abs(mean_valrank - mean_width)

    n = random.randint(5, 40)
    d = random.randint(1, n-1)
    graph = generate_d_regular_graph(n, d)
    
    if graph is None:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    valrank = p_adic_valuation_rank(graph)
    width = frege_proof_width(graph)
    
    return {
        "metric_name": "correlation",
        "metric_value": calculate_correlation_and_mean_difference([valrank], [width])[0],
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if "conjecture_holds" not in r or r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if 'counterexample' in r)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")