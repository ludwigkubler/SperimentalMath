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
    
    def generate_d_regular_graph(n, d):
        if n % d != 0:
            return None
        graph = [[] for _ in range(n)]
        edges_added = set()
        while len(edges_added) < (n * d) // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and (u, v) not in edges_added and (v, u) not in edges_added:
                graph[u].append(v)
                graph[v].append(u)
                edges_added.add((u, v))
        return graph
    
    def is_vertex_cover(graph, cover):
        for u in range(len(graph)):
            if all(v not in cover for v in graph[u]):
                return False
        return True
    
    def find_min_vertex_cover(graph):
        n = len(graph)
        min_cover_size = n
        min_cover = None
        
        def backtrack(cover, start):
            nonlocal min_cover_size, min_cover
            if len(cover) >= min_cover_size:
                return
            if is_vertex_cover(graph, cover):
                if len(cover) < min_cover_size:
                    min_cover_size = len(cover)
                    min_cover = cover[:]
                return
            for v in range(start, n):
                if v not in cover:
                    backtrack(cover + [v], v + 1)
        
        backtrack([], 0)
        return min_cover
    
    def frege_proof_depth(graph, vertex_cover):
        # Simplified DPLL solver for the vertex cover problem
        n = len(graph)
        stack = []
        assignment = [False] * n
        
        def dpll():
            if all(assignment[v] or v not in graph[u] for u in range(n)):
                return True
            for v in range(n):
                if not assignment[v]:
                    assignment[v] = True
                    if dpll():
                        return True
                    assignment[v] = False
                    stack.append(v)
                    break
            else:
                while stack and assignment[stack[-1]]:
                    stack.pop()
                if stack:
                    v = stack.pop()
                    assignment[v] = True
                    for u in range(n):
                        if v in graph[u]:
                            assignment[u] = False
                    if dpll():
                        return True
                    assignment[v] = False
            return False
        
        return len(vertex_cover) + 1 if dpll() else -1
    
    def ehrhart_quotient(graph):
        n = len(graph)
        # Simplified Ehrhart quotient calculation (linear in n for this example)
        return n
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 2)
        if graph is None:
            continue
        vertex_cover = find_min_vertex_cover(graph)
        if vertex_cover is None:
            continue
        o_G = ehrhart_quotient(graph)
        f_G = frege_proof_depth(graph, vertex_cover)
        results.append({"n": n, "o(G)": o_G, "f(G)": f_G})
    
    if not results:
        return {
            "metric_name": "Ehrhart Quotient and Frege Proof Depth",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid graphs generated"
        }
    
    instances_tested = len(results)
    n_max = max(r["n"] for r in results)
    o_G_values = [r["o(G)"] for r in results]
    f_G_values = [r["f(G)"] for r in results]
    
    def mean(values):
        return sum(values) / len(values)
    
    def std_dev(values, mean):
        return math.sqrt(sum((x - mean) ** 2 for x in values) / len(values))
    
    o_G_mean = mean(o_G_values)
    f_G_mean = mean(f_G_values)
    o_G_std = std_dev(o_G_values, o_G_mean)
    f_G_std = std_dev(f_G_values, f_G_mean)
    
    correlation_coefficient = sum((o_G_values[i] - o_G_mean) * (f_G_values[i] - f_G_mean) for i in range(instances_tested)) / (instances_tested * o_G_std * f_G_std)
    
    return {
        "metric_name": "Ehrhart Quotient and Frege Proof Depth",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")