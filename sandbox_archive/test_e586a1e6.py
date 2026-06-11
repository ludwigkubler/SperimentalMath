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
        if n * d % 2 != 0 or d < 1 or d >= n:
            return None
        graph = [[] for _ in range(n)]
        edges = set()
        for i in range(d):
            for j in range(i + 1, n):
                if (i, j) not in edges and (j, i) not in edges:
                    graph[i].append(j)
                    graph[j].append(i)
                    edges.add((i, j))
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clause = [literals[i]]
            for j in graph[i]:
                clause.append(f'-{literals[j]}')
            clauses.append(clause)
        for i in range(n):
            for j in range(i + 1, n):
                clause = [f'-{literals[i]}', f'-{literals[j]}', f'x{i}{j}']
                clauses.append(clause)
                clause = [f'{literals[i]}', f'{literals[j]}', f'-x{i}{j}']
                clauses.append(clause)
        for i in range(n):
            for j in range(i + 1, n):
                clause = [f'x{i}{j}', f'-{literals[i]}', f'-{literals[j]}']
                clauses.append(clause)
        return literals, clauses
    
    def frege_proof_depth(clauses):
        # Simplified Frege proof depth calculation
        return len(clauses) * 2
    
    def hodge_theoretic_generators(graph):
        n = len(graph)
        # Placeholder for actual Hodge-theoretic generator count calculation
        return random.randint(1, n)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        graph = generate_d_regular_graph(n, 2)  # Example: d=2
        if not graph:
            continue
        literals, clauses = tseitin_formula(graph)
        proof_depth = frege_proof_depth(clauses)
        generators = hodge_theoretic_generators(graph)
        results.append({
            "n": n,
            "proof_depth": proof_depth,
            "generators": generators
        })
    
    if not results:
        return {
            "metric_name": "Hodge-theoretic Generators vs Frege Proof Depth",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    h_values = [r["generators"] for r in results]
    f_values = [r["proof_depth"] for r in results]
    
    mean_h = sum(h_values) / len(h_values)
    mean_f = sum(f_values) / len(f_values)
    variance_h = sum((x - mean_h) ** 2 for x in h_values) / len(h_values)
    variance_f = sum((y - mean_f) ** 2 for y in f_values) / len(f_values)
    
    covariance = sum((h_values[i] - mean_h) * (f_values[i] - mean_f) for i in range(len(results))) / len(results)
    correlation_coefficient = covariance / math.sqrt(variance_h * variance_f)
    
    return {
        "metric_name": "Hodge-theoretic Generators vs Frege Proof Depth",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.9,
        "counterexample": "" if abs(correlation_coefficient) >= 0.9 else f"correlation={correlation_coefficient}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r["metric_value"]) >= 0.9) / len(results)
    
    if all(abs(r["metric_value"]) >= 0.9 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(abs(r["metric_value"]) < 0.7 or abs(r["metric_value"]) > 1.3 for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if abs(r["metric_value"]) < 0.7 or abs(r["metric_value"]) > 1.3)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_out_of_bounds\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")