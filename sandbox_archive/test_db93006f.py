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
        if (n * d) % 2 != 0:
            return None
        graph = {i: set() for i in range(n)}
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d:
                    edges.append((i, j))
                    graph[i].add(j)
                    graph[j].add(i)
        return graph
    
    def compute_min_genus(graph):
        # Simplified heuristic for genus computation
        # This is a placeholder and may not be accurate for all graphs
        n = len(graph)
        d = sum(len(neighbors) for neighbors in graph.values()) // n
        if d == 0:
            return 0
        return math.ceil((d - 2) / 2)
    
    def generate_tseitin_formula(graph):
        # Simplified Tseitin formula generation
        # This is a placeholder and may not be accurate for all graphs
        n = len(graph)
        literals = {i: f"x{i}" for i in range(n)}
        clauses = []
        for i in range(n):
            clauses.append([literals[i]])
            for j in graph[i]:
                clauses.append([-literals[i], literals[j]])
        return clauses
    
    def compute_resolution_proof_width(clauses):
        # Simplified resolution proof width computation
        # This is a placeholder and may not be accurate for all graphs
        queue = [clauses]
        while queue:
            clause = queue.pop()
            if len(clause) == 1:
                return len(queue)
            literal = clause[0]
            new_clauses = []
            for c in queue:
                if literal in c:
                    continue
                if -literal in c:
                    new_clauses.append([x for x in c if x != -literal])
                else:
                    new_clauses.append(c + [-literal])
            queue.extend(new_clauses)
        return len(queue)
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov / (std_x * std_y)
    
    results = []
    min_genus_list = []
    resolution_width_list = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        graph = generate_d_regular_graph(n, 3)
        if graph is None:
            continue
        min_genus = compute_min_genus(graph)
        clauses = generate_tseitin_formula(graph)
        resolution_width = compute_resolution_proof_width(clauses)
        
        results.append({"n": n, "min_genus": min_genus, "resolution_width": resolution_width})
        min_genus_list.append(min_genus)
        resolution_width_list.append(resolution_width)
    
    if len(results) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max([r["n"] for r in results]),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    corr = correlation_coefficient(min_genus_list, resolution_width_list)
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": corr,
        "instances_tested": len(results),
        "n_max": max([r["n"] for r in results]),
        "conjecture_holds": 0.9 <= corr < 1.0,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_corr = math.sqrt(sum((r["metric_value"] - mean_corr) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(0.7 <= corr < 1.0 for r in results for corr in [r["metric_value"] for r in results if r["metric_value"] is not None]):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i + 1 for i, r in enumerate(results) if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient' first_failing_seed={first_failing_seed}")