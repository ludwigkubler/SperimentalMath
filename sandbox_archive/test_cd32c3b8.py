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
        edges_added = set()
        for _ in range(d * n // 2):
            while True:
                u = random.randint(0, n - 1)
                v = random.randint(0, n - 1)
                if u == v or (u, v) in edges_added or (v, u) in edges_added:
                    continue
                graph[u].append(v)
                graph[v].append(u)
                edges_added.add((u, v))
                break
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = {i: f"x{i}" for i in range(n)}
        clauses = []
        for i in range(n):
            clause = [literals[i]]
            for j in graph[i]:
                clause.append(f"¬{literals[j]}")
            clauses.append(clause)
        for i in range(n):
            for j in range(i + 1, n):
                clause = [f"¬{literals[i]}", f"¬{literals[j]}"]
                for k in graph[i]:
                    if k != j:
                        clause.append(literals[k])
                clauses.append(clause)
        return clauses
    
    def topological_degree(graph):
        n = len(graph)
        degrees = [len(neighbors) for neighbors in graph.values()]
        return sum(degrees) // n
    
    def frege_proof_size(clauses):
        # Simplistic estimation based on clause count
        return len(clauses)
    
    n_max = 40
    instances_tested = 0
    correlation_sum = 0
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            break
        for _ in range(5):
            graph = generate_d_regular_graph(n, 2)
            if graph is None:
                continue
            clauses = tseitin_formula(graph)
            td = topological_degree(graph)
            f = frege_proof_size(clauses)
            correlation_sum += abs(td - f)
            instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    correlation = correlation_sum / instances_tested
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation) <= 2,
        "counterexample": "" if abs(correlation) <= 2 else f"correlation={correlation}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if abs(r["metric_value"]) <= 2) / len(results)
    
    if all(abs(r["metric_value"]) <= 5 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(abs(r["metric_value"]) > 5 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if abs(result["metric_value"]) > 5)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_exceeds_5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")