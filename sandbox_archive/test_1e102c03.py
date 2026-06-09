# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
from math import gcd
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0:
            return None
        graph = {i: set() for i in range(n)}
        edges = list(combinations(range(n), 2))
        random.shuffle(edges)
        for edge in edges[:d * n // 2]:
            u, v = edge
            if len(graph[u]) < d and len(graph[v]) < d:
                graph[u].add(v)
                graph[v].add(u)
        return graph
    
    def p_adic_valuation_rank(graph):
        if not graph:
            return 0
        n = len(graph)
        values = [Fraction(1, 2) for _ in range(n)]
        rank = 0
        while True:
            changed = False
            for u in range(n):
                for v in graph[u]:
                    if values[v].numerator % 2 == 1:
                        values[v] *= Fraction(1, 2)
                        changed = True
            if not changed:
                break
            rank += 1
        return rank
    
    def frege_proof_width(graph):
        if not graph:
            return 0
        n = len(graph)
        width = 0
        for u in range(n):
            for v in graph[u]:
                width = max(width, abs(u - v))
        return width
    
    n_max = 40
    instances_tested = 30
    valranks = []
    widths = []
    
    for _ in range(instances_tested):
        d = random.randint(2, min(n_max // 2, 10))
        graph = generate_d_regular_graph(n_max, d)
        if not graph:
            continue
        valrank = p_adic_valuation_rank(graph)
        width = frege_proof_width(graph)
        valranks.append(valrank)
        widths.append(width)
    
    if len(valranks) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(valranks),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_valrank = sum(valranks) / len(valranks)
    mean_width = sum(widths) / len(widths)
    correlation_coefficient = 0
    numerator = sum((valranks[i] - mean_valrank) * (widths[i] - mean_width) for i in range(len(valranks)))
    denominator = sum((valranks[i] - mean_valrank)**2 * (widths[i] - mean_width)**2 for i in range(len(valranks)))**0.5
    if denominator == 0:
        correlation_coefficient = None
    else:
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and abs(mean_valrank - mean_width) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = (sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))**0.5
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")