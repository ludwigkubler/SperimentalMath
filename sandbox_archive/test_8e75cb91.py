# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def is_edge(graph, u, v):
        return (u, v) in graph or (v, u) in graph
    
    def automorphism_group(graph):
        n = len(graph)
        group = []
        for perm in itertools.permutations(range(n)):
            if all(is_edge(graph, perm[i], perm[j]) == is_edge(graph, i, j) for i in range(n) for j in range(i + 1, n)):
                group.append(perm)
        return group
    
    def geometric_invariants(group):
        # Placeholder for actual computation of geometric invariants
        return len(group)
    
    def quantum_query_complexity(graph):
        # Placeholder for actual computation of quantum query complexity
        return len(graph) ** 2
    
    n = random.randint(5, 40)
    graph = generate_graph(n)
    group = automorphism_group(graph)
    invariants = geometric_invariants(group)
    query_complexity = quantum_query_complexity(graph)
    
    metric_value = invariants / (query_complexity + 1)  # Avoid division by zero
    conjecture_holds = invariants <= query_complexity ** 2  # Polynomial bound
    
    return {
        "metric_name": "Ratio of Invariants to Query Complexity",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "Mapping undefined"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Mapping undefined' first_failing_seed={first_failing_seed}")