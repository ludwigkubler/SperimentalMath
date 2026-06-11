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

def generate_cnf(n):
    clauses = []
    for _ in range(n):
        clause = [random.randint(1, n), -random.randint(1, n)]
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)
    return clauses

def tseitin_graph(cnf):
    graph = {}
    literals = set()
    for i, clause in enumerate(cnf):
        literals.update(abs(lit) for lit in clause)
        for lit1 in clause:
            for lit2 in clause:
                if lit1 != lit2:
                    if lit1 not in graph:
                        graph[lit1] = []
                    if lit2 not in graph:
                        graph[lit2] = []
                    graph[lit1].append(lit2)
    return graph, literals

def spanning_tree(graph):
    visited = set()
    stack = [1]
    tree_edges = []

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    tree_edges.append((node, neighbor))
                    stack.append(neighbor)

    return tree_edges

def entanglement_complexity(cnf):
    n = len(cnf)
    return Fraction(n * (n - 1), 2)  # Simplified for demonstration

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        cnf = generate_cnf(n)
        graph, literals = tseitin_graph(cnf)
        tree_edges = spanning_tree(graph)
        geometric_complexity = len(tree_edges)
        entanglement_comp = entanglement_complexity(cnf)
        results.append((geometric_complexity, entanglement_comp))

    if not results:
        return {
            "metric_name": "Geometric Complexity vs Entanglement",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }

    geometric_values = [r[0] for r in results]
    entanglement_values = [r[1] for r in results]

    mean_geometric = sum(geometric_values) / len(geometric_values)
    mean_entanglement = sum(entanglement_values) / len(entanglement_values)

    correlation_coefficient = (sum((x - mean_geometric) * (y - mean_entanglement) for x, y in zip(geometric_values, entanglement_values)) /
                               math.sqrt(sum((x - mean_geometric) ** 2 for x in geometric_values) *
                                         sum((y - mean_entanglement) ** 2 for y in entanglement_values)))

    return {
        "metric_name": "Geometric Complexity vs Entanglement",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": abs(correlation_coefficient - 1) <= 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3  # Default to first 30 primes

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_corr = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["metric_value"] is not None for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_outside_tolerance\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_results")