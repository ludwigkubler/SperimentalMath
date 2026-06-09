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
    
    def generate_cnf(n):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(n):
            clause = [random.choice(variables), -random.choice(variables)]
            clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        stack = cnf[:]
        while True:
            new_clauses = []
            found_resolvent = False
            for i in range(len(stack)):
                for j in range(i + 1, len(stack)):
                    if -stack[i][0] in stack[j]:
                        resolvent = [x for x in stack[i] if x != -stack[i][0]] + [x for x in stack[j] if x != -stack[i][0]]
                        new_clauses.append(resolvent)
                        found_resolvent = True
            if not found_resolvent:
                break
            stack.extend(new_clauses)
        return len(stack)
    
    def cayley_graph_diameter(cnf):
        n = len(cnf)
        graph = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if -cnf[i][0] in cnf[j]:
                    graph[i][j] = 1
                    graph[j][i] = 1
        def bfs(start):
            visited = [False] * n
            queue = [(start, 0)]
            while queue:
                node, dist = queue.pop(0)
                if not visited[node]:
                    visited[node] = True
                    for neighbor in range(n):
                        if graph[node][neighbor] == 1 and not visited[neighbor]:
                            queue.append((neighbor, dist + 1))
            return max(dist for dist in range(n) if visited[dist])
        return bfs(0)
    
    n_values = [5, 10, 15, 20, 30, 40]
    widths = []
    diameters = []
    for n in n_values:
        cnf = generate_cnf(n)
        width = resolution_width(cnf)
        diameter = cayley_graph_diameter(cnf)
        widths.append(width)
        diameters.append(diameter)
    
    correlation_coefficient = sum((widths[i] - mean_w) * (diameters[i]**2 - mean_d**2) for i in range(len(n_values))) / len(n_values)
    mean_w = sum(widths) / len(widths)
    mean_d_squared = sum(d ** 2 for d in diameters) / len(diameters)
    
    conjecture_holds = correlation_coefficient >= 0.8 and mean_w / mean_d_squared <= 1
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")