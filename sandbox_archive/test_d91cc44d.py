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
            raise ValueError("Graph size must be a multiple of the degree")
        graph = {i: [] for i in range(n)}
        edges_added = set()
        while len(edges_added) < (n * d) // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and (u, v) not in edges_added and (v, u) not in edges_added:
                graph[u].append(v)
                graph[v].append(u)
                edges_added.add((u, v))
        return graph

    def tseitin_formula(graph):
        n = len(graph)
        clauses = []
        literals = {}
        for i in range(n):
            literals[i] = f"x{i}"
        
        def add_clause(clause):
            clauses.append(clause)
        
        for i in range(n):
            clause = [f"~{literals[i]}"]
            for j in graph[i]:
                clause.append(literals[j])
            add_clause(clause)
        
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    clause = [f"~{literals[i]}", f"~{literals[j]}", literals[k]]
                    add_clause(clause)
                    clause = [f"~{literals[i]}", f"~{literals[k]}", literals[j]]
                    add_clause(clause)
                    clause = [f"~{literals[j]}", f"~{literals[k]}", literals[i]]
                    add_clause(clause)
        
        return clauses

    def frege_proof_depth(clauses):
        n = len(clauses)
        if n == 0:
            return 0
        depth = [1] * n
        for i in range(n):
            for clause in clauses[i]:
                if clause.startswith("~"):
                    j = int(clause[1:])
                    depth[j - 1] += 1
        return max(depth)

    def local_zeta_function_order(graph):
        n = len(graph)
        zeta_values = [0] * (n + 1)
        for i in range(n):
            zeta_values[i + 1] = sum(1 / (i + 1) for i in graph[i])
        return max(zeta_values)

    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)

    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        d = random.randint(2, min(n - 1, 6))
        graph = generate_d_regular_graph(n, d)
        clauses = tseitin_formula(graph)
        proof_depth = frege_proof_depth(clauses)
        zeta_order = local_zeta_function_order(graph)
        results.append((zeta_order, proof_depth))

    metric_value = correlation_coefficient([x for x, _ in results], [y for _, y in results])
    conjecture_holds = abs(metric_value) > 0.8
    counterexample = "" if conjecture_holds else "correlation_coefficient"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_evidence")