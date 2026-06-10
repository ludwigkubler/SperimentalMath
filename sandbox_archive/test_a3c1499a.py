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
    
    def generate_d_regular_graph(d, n):
        if d * (n - 1) % 2 != 0:
            return None
        graph = [[] for _ in range(n)]
        edges = set()
        for i in range(1, n):
            for j in range(i):
                if len(graph[j]) < d and len(graph[i]) < d:
                    edge = (i, j)
                    if edge not in edges and (j, i) not in edges:
                        graph[i].append(j)
                        graph[j].append(i)
                        edges.add(edge)
        return graph

    def tseitin_formula(graph):
        n = len(graph)
        literals = [f"x{i}" for i in range(n)]
        clauses = []
        for i, neighbors in enumerate(graph):
            clause = [literals[i]]
            for j in neighbors:
                clause.append(f"~{literals[j]}")
            clauses.append(clause)
            for j in range(i + 1, n):
                if j not in neighbors and (i, j) not in graph[j]:
                    clause = []
                    clause.append(literals[i])
                    clause.append(f"~{literals[j]}")
                    clause.append(f"x{j}")
                    clauses.append(clause)
        return literals, clauses

    def kostant_multi_index(formula):
        # Placeholder for the actual computation of Kostant multi-index
        # This is a dummy implementation that returns a random value
        return random.random()

    def resolution_proof_width(formula):
        # Placeholder for the actual computation of resolution proof width
        # This is a dummy implementation that returns a random value
        return random.randint(1, 10)

    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        graph = generate_d_regular_graph(3, n)
        if graph is None:
            continue
        literals, clauses = tseitin_formula(graph)
        kmi_value = kostant_multi_index((literals, clauses))
        wp_value = resolution_proof_width((literals, clauses))
        results.append({"kmi": kmi_value, "wp": wp_value})

    if len(results) < 100:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }

    kmi_values = [r["kmi"] for r in results]
    wp_values = [r["wp"] for r in results]
    mean_kmi = sum(kmi_values) / len(kmi_values)
    mean_wp = sum(wp_values) / len(wp_values)
    covariance = sum((kmi - mean_kmi) * (wp - mean_wp) for kmi, wp in zip(kmi_values, wp_values)) / len(kmi_values)
    variance_kmi = sum((kmi - mean_kmi) ** 2 for kmi in kmi_values) / len(kmi_values)
    variance_wp = sum((wp - mean_wp) ** 2 for wp in wp_values) / len(wp_values)
    correlation_coefficient = covariance / math.sqrt(variance_kmi * variance_wp)

    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8,
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

    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_too_low\" first_failing_seed={first_failing_seed}")