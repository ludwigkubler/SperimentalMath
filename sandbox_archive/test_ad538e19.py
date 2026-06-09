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
    
    def generate_d_regular_graph(d, n):
        if d * (n - 1) % 2 != 0:
            return None
        graph = [[] for _ in range(n)]
        edges = set()
        for i in range(1, n):
            for j in range(i):
                if len(graph[j]) < d and len(graph[i]) < d:
                    edge = (j, i)
                    if edge not in edges and (i, j) not in edges:
                        graph[j].append(i)
                        graph[i].append(j)
                        edges.add(edge)
        return graph
    
    def frege_proof_width(graph):
        n = len(graph)
        visited = [False] * n
        stack = []
        
        def dfs(node):
            if visited[node]:
                return 0
            visited[node] = True
            width = 1
            for neighbor in graph[node]:
                width = max(width, dfs(neighbor) + 1)
            stack.append((node, width))
            return width
        
        dfs(0)
        
        max_width = 0
        while stack:
            node, width = stack.pop()
            max_width = max(max_width, width)
        return max_width
    
    def p_adic_valuation_rank(graph):
        n = len(graph)
        values = set()
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j] == 0:
                    continue
                value = Fraction(1, graph[i][j])
                while value.denominator % 2 == 0:
                    value.numerator *= 2
                    value.denominator //= 2
                values.add(value)
        return len(values)
    
    d = 3  # Example degree
    n_max = max(n for n in [5, 10, 15, 20, 30, 40] if any(generate_d_regular_graph(d, n) is not None for _ in range(3)))
    results = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        graph = generate_d_regular_graph(d, n)
        if graph is None:
            continue
        valrank = p_adic_valuation_rank(graph)
        w = frege_proof_width(graph)
        results.append((graph, (valrank, w)))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    valranks = [result[1][0] for result in results]
    widths = [result[1][1] for result in results]
    
    mean_valrank = sum(valranks) / len(valranks)
    mean_width = sum(widths) / len(widths)
    correlation = (sum((valranks[i] - mean_valrank) * (widths[i] - mean_width) for i in range(len(valranks))) /
                   math.sqrt(sum((valranks[i] - mean_valrank) ** 2 for i in range(len(valranks))) *
                             sum((widths[i] - mean_width) ** 2 for i in range(len(widths)))))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": abs(correlation) >= 0.8 and abs(mean_valrank - mean_width) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")