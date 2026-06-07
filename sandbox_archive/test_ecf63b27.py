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
        if n % d != 0:
            return None
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
    
    def calculate_mrl(graph):
        n = len(graph)
        degrees = [len(neighbors) for neighbors in graph.values()]
        mrl = sum(degrees) / (2 * n)
        return mrl
    
    def generate_random_sat_instance(graph):
        n = len(graph)
        variables = list(range(n))
        clauses = []
        for u in range(n):
            clause = [random.choice([-1, 1]) * v for v in graph[u]]
            clauses.append(clause)
        sat_instance = (variables, clauses)
        return sat_instance
    
    def calculate_resolution_width(sat_instance):
        variables, clauses = sat_instance
        n = len(variables)
        resolution_width = 0
        queue = [clauses]
        while queue:
            new_clause = []
            for clause in queue.pop(0):
                if not clause:
                    return resolution_width
                literal = random.choice(clause)
                new_clause.extend([l for l in clause if l != literal and -l not in clause])
            queue.append(new_clause)
            resolution_width += 1
        return resolution_width
    
    n_values = [5, 10, 15, 20, 30, 40]
    mrls = []
    widths = []
    
    for n in n_values:
        graph = generate_d_regular_graph(n, 2)
        if graph is None:
            continue
        mrl = calculate_mrl(graph)
        sat_instance = generate_random_sat_instance(graph)
        width = calculate_resolution_width(sat_instance)
        mrls.append(mrl)
        widths.append(width)
    
    if len(mrls) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(mrls),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    correlation = sum((mrl - m_avg) * (width - w_avg) for mrl, width in zip(mrls, widths)) / len(mrls)
    m_avg = sum(mrls) / len(mrls)
    w_avg = sum(widths) / len(widths)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": 30,
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.5,
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
    
    mean_corr = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    elif any(r["metric_value"] < 0.3 or r["p_value"] > 0.1 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")