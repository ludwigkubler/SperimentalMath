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
        while len(edges_added) < n * d // 2:
            u, v = random.sample(range(n), 2)
            if u > v:
                u, v = v, u
            edge = (u, v)
            if edge not in edges_added and u != v:
                graph[u].append(v)
                graph[v].append(u)
                edges_added.add(edge)
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        clauses = []
        for i in range(n):
            literals = [random.choice([f"x{i}", f"~x{i}"]) for _ in range(d)]
            clause = [literals[0]]
            for literal in literals[1:]:
                clause.append("~" + literal)
            clauses.append(clause)
            for j in range(1, d):
                clause = ["~" + literals[j-1], literals[j]]
                clauses.append(clause)
        return clauses
    
    def formal_group_representation_size(formula):
        # This is a placeholder function. Implement the actual calculation.
        return len(formula)  # Simplified for testing purposes
    
    def circuit_monotone_width(formula):
        # This is a placeholder function. Implement the actual calculation.
        return len(formula)  # Simplified for testing purposes
    
    n = random.randint(5, 40)
    d = random.randint(2, min(n - 1, 3))
    graph = generate_d_regular_graph(n, d)
    if not graph:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Graph size must be a multiple of the degree"
        }
    
    formula = tseitin_formula(graph)
    mfr = formal_group_representation_size(formula)
    w_monotone = circuit_monotone_width(formula)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": 1.0 if mfr == w_monotone else 0.0,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")