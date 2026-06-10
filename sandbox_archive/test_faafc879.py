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
        graph = [[] for _ in range(n)]
        edges_added = set()
        for i in range(n):
            neighbors = random.sample(range(n), d - len(graph[i]))
            for neighbor in neighbors:
                if (i, neighbor) not in edges_added and (neighbor, i) not in edges_added:
                    graph[i].append(neighbor)
                    graph[neighbor].append(i)
                    edges_added.add((i, neighbor))
        return graph

    def calculate_geoc(graph):
        n = len(graph)
        degree_sum = sum(len(neighbors) for neighbors in graph)
        if degree_sum == 0:
            return 0
        geoc = degree_sum / (n * (n - 1))
        return geoc

    def calculate_circuit_size(graph):
        n = len(graph)
        edges = set()
        for i in range(n):
            for neighbor in graph[i]:
                if (i, neighbor) not in edges and (neighbor, i) not in edges:
                    edges.add((i, neighbor))
        return len(edges)

    n_values = [5, 10, 15, 20, 30, 40]
    geoc_sum = 0
    circuit_size_sum = 0
    instances_tested = 0

    for n in n_values:
        for _ in range(5):
            d = random.randint(2, min(n - 1, 3))
            graph = generate_d_regular_graph(n, d)
            if graph is None:
                continue
            geoc = calculate_geoc(graph)
            circuit_size = calculate_circuit_size(graph)
            geoc_sum += geoc
            circuit_size_sum += circuit_size
            instances_tested += 1

    mean_geoc = geoc_sum / instances_tested
    mean_circuit_size = circuit_size_sum / instances_tested
    correlation_coefficient = (instances_tested * sum(geoc * circuit_size for geoc, circuit_size in zip(range(instances_tested), range(instances_tested)))
                               - instances_tested * mean_geoc * mean_circuit_size) / math.sqrt(
        (instances_tested * sum(geoc ** 2 for geoc in range(instances_tested)) - instances_tested * mean_geoc ** 2)
        * (instances_tested * sum(circuit_size ** 2 for circuit_size in range(instances_tested)) - instances_tested * mean_circuit_size ** 2))

    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": "" if correlation_coefficient >= 0.8 else "Pearson correlation coefficient < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.6f} std=0.000000 support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation coefficient < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")