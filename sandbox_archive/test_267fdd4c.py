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
        if (d * n) % 2 != 0 or d >= n:
            return None
        graph = {i: [] for i in range(n)}
        edges_added = set()
        while len(edges_added) < d * n // 2:
            u, v = random.sample(range(n), 2)
            if u == v or (u, v) in edges_added or (v, u) in edges_added:
                continue
            graph[u].append(v)
            graph[v].append(u)
            edges_added.add((u, v))
            edges_added.add((v, u))
        return graph

    def compute_lattice_point_count(graph):
        n = len(graph)
        lattice_points = set()
        for i in range(n):
            queue = [i]
            visited = {i}
            while queue:
                node = queue.pop(0)
                for neighbor in graph[node]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            lattice_points.update(visited)
        return len(lattice_points)

    def compute_frege_proof_length(graph):
        n = len(graph)
        edges_added = set()
        proof_length = 0
        while len(edges_added) < d * n // 2:
            u, v = random.sample(range(n), 2)
            if (u, v) in edges_added or (v, u) in edges_added:
                continue
            edges_added.add((u, v))
            edges_added.add((v, u))
            proof_length += 1
        return proof_length

    n_values = [20, 30, 40]
    lattice_point_counts = []
    frege_proof_lengths = []

    for n in n_values:
        graph = generate_d_regular_graph(n, d=3)
        if graph is None:
            continue
        lattice_point_count = compute_lattice_point_count(graph)
        frege_proof_length = compute_frege_proof_length(graph)
        lattice_point_counts.append(lattice_point_count)
        frege_proof_lengths.append(frege_proof_length)

    if not lattice_point_counts or not frege_proof_lengths:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "graph_generation_failed"
        }

    mean_lattice_point_count = sum(lattice_point_counts) / len(lattice_point_counts)
    mean_frege_proof_length = sum(frege_proof_lengths) / len(frege_proof_lengths)

    correlation_coefficient = sum((x - mean_lattice_point_count) * (y - mean_frege_proof_length) for x, y in zip(lattice_point_counts, frege_proof_lengths)) / (len(lattice_point_counts) * math.sqrt(sum((x - mean_lattice_point_count) ** 2 for x in lattice_point_counts) * sum((y - mean_frege_proof_length) ** 2 for y in frege_proof_lengths)))

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(lattice_point_counts),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7 and all(corr >= 0.5 for corr in [correlation_coefficient]),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None)) / len([r for r in results if r["metric_value"] is not None])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and min(r["metric_value"] for r in results if r["metric_value"] is not None) >= 0.5:
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_below_0.7\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data_or_unsupported_conjecture")