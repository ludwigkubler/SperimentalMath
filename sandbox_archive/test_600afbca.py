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
        if (n * d) % 2 != 0:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        while len(edges) < n * d // 2:
            u, v = random.sample(range(n), 2)
            if u == v or (u, v) in edges or (v, u) in edges:
                continue
            graph[u].append(v)
            graph[v].append(u)
            edges.add((u, v))
        return graph
    
    def compute_genus(graph):
        n = len(graph)
        m = sum(len(neighbors) for neighbors in graph.values()) // 2
        if n == 0:
            return 0
        genus = (n - m + 1) / 2
        return int(math.ceil(genus))
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = {i: f'x{i}' for i in range(n)}
        clauses = []
        for u, neighbors in graph.items():
            clause = [f'-{literals[u]}']
            for v in neighbors:
                clause.append(f'{literals[v]}')
            clauses.append(clause)
        return clauses
    
    def resolution_width(clauses):
        stack = []
        visited = set()
        for clause in clauses:
            if not any(lit.startswith('-') and lit[1:] in visited for lit in clause):
                stack.append(clause)
        
        while stack:
            current_clause = stack.pop()
            new_clauses = []
            for other_clause in clauses:
                common_lit = next((lit for lit in current_clause if lit.startswith('-') and lit[1:] in other_clause), None)
                if common_lit:
                    new_clause = [lit for lit in current_clause if lit != common_lit] + [lit for lit in other_clause if not lit.startswith('-') and lit != common_lit]
                    if len(new_clause) == 0:
                        return float('inf')
                    new_clauses.append(new_clause)
            clauses.extend(new_clauses)
        
        return len(clauses)
    
    def run_graph_trial(n, d):
        graph = generate_d_regular_graph(n, d)
        if not graph:
            return None
        genus = compute_genus(graph)
        clauses = tseitin_formula(graph)
        width = resolution_width(clauses)
        return {"genus": genus, "width": width}
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        for _ in range(5):
            result = run_graph_trial(n, random.randint(3, min(n-1, 8)))
            if result is not None:
                results.append(result)
    
    if len(results) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": float('nan'),
            "instances_tested": len(results),
            "n_max": max(n for n, _ in n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    genus = [r["genus"] for r in results]
    width = [r["width"] for r in results]
    correlation_coefficient = sum((g - mean_genus) * (w - mean_width) for g, w in zip(genus, width)) / len(results)
    mean_genus = sum(genus) / len(genus)
    mean_width = sum(width) / len(width)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in n_values),
        "conjecture_holds": 0.7 <= correlation_coefficient <= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print("RESULT: FALSIFIED counterexample=\"correlation_coefficient_out_of_range\" first_failing_seed=<s>")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support support_fraction={support_fraction}")