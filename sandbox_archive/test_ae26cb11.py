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
        if (n * d) % 2 != 0 or d >= n:
            return None
        graph = [[] for _ in range(n)]
        edges_used = set()
        for i in range(d):
            for j in range(i + 1, n):
                if (i, j) not in edges_used and (j, i) not in edges_used:
                    graph[i].append(j)
                    graph[j].append(i)
                    edges_used.add((i, j))
        return graph
    
    def tseitin_formula(graph, n):
        clauses = []
        literals = {}
        for v in range(n):
            literals[v] = random.randint(1, 2 * n)
        for v in range(n):
            clauses.append([literals[v]])
            for u in graph[v]:
                clauses.append([-literals[v], literals[u]])
        return clauses
    
    def resolution_width(clauses):
        queue = clauses[:]
        learned_clauses = []
        while queue:
            clause1 = queue.pop()
            if len(clause1) == 0:
                return float('inf')
            for clause2 in queue + learned_clauses:
                if len(clause2) == 0:
                    return float('inf')
                for literal in clause1:
                    if -literal in clause2:
                        new_clause = [l for l in clause2 if l != -literal]
                        if new_clause not in queue and new_clause not in learned_clauses:
                            learned_clauses.append(new_clause)
                            break
        return max(len(clause) for clause in learned_clauses)
    
    def alexander_orlik_solomon_complexity(graph):
        n = len(graph)
        generators = set()
        for v in range(n):
            for u in graph[v]:
                if v < u:
                    generators.add((v, u))
        return len(generators)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        d = random.randint(1, min(n - 1, 2))
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            continue
        clauses = tseitin_formula(graph, n)
        width = resolution_width(clauses)
        complexity = alexander_orlik_solomon_complexity(graph)
        results.append({
            "n": n,
            "d": d,
            "complexity": complexity,
            "width": width
        })
    
    if not results:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    total_complexity = sum(result["complexity"] for result in results)
    total_width = sum(result["width"] for result in results)
    mean_complexity = total_complexity / len(results)
    mean_width = total_width / len(results)
    
    if any(abs(result["complexity"] - result["width"]) > 10 for result in results):
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "discrepancy_greater_than_10"
        }
    
    if any(abs(mean_complexity - mean_width) > 3 * (mean_width / len(results)) for _ in range(10)):
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "correlation_factor_greater_than_3"
        }
    
    return {
        "metric_name": "resolution_width",
        "metric_value": mean_complexity,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(result["counterexample"] == "discrepancy_greater_than_10" for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"] == "discrepancy_greater_than_10")
        print(f"RESULT: FALSIFIED counterexample=\"discrepancy_greater_than_10\" first_failing_seed={first_failing_seed}")
    elif any(result["counterexample"] == "correlation_factor_greater_than_3" for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"] == "correlation_factor_greater_than_3")
        print(f"RESULT: FALSIFIED counterexample=\"correlation_factor_greater_than_3\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")