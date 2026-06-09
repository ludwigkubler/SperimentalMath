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
        if (n * d) % 2 != 0:
            return None
        graph = [set() for _ in range(n)]
        edges_added = set()
        while len(edges_added) < n * d // 2:
            u = random.randint(0, n-1)
            v = random.randint(0, n-1)
            if u != v and (u, v) not in edges_added and (v, u) not in edges_added:
                graph[u].add(v)
                graph[v].add(u)
                edges_added.add((u, v))
        return graph
    
    def compute_circuit_complexity(graph):
        n = len(graph)
        # Simplified heuristic for circuit complexity
        return n * (n - 1) // 2
    
    def braided_quantum_group_representation(graph):
        n = len(graph)
        if n == 0:
            return 0
        dim = 1
        for i in range(n):
            dim *= (n - graph[i].__len__())
        return dim
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov / (std_x * std_y)
    
    def p_value(r, n):
        if r >= 0:
            z = (r * math.sqrt(n - 2)) / math.sqrt(1 - r**2)
        else:
            z = -(r * math.sqrt(n - 2)) / math.sqrt(1 - r**2)
        return 2 * (1 - 0.5 * (1 + math.erf(z / math.sqrt(2))))
    
    n_max = 40
    instances_tested = 0
    dim_values = []
    circuit_complexity_values = []
    
    for n in range(5, n_max + 1):
        if n > 30:
            break
        graph = generate_d_regular_graph(n, 2)
        if graph is None:
            continue
        instances_tested += 1
        dim = braided_quantum_group_representation(graph)
        circuit_complexity = compute_circuit_complexity(graph)
        dim_values.append(dim)
        circuit_complexity_values.append(circuit_complexity)
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    r = correlation_coefficient(dim_values, circuit_complexity_values)
    p = p_value(r, instances_tested)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": r,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": p < 0.05 and abs(r) >= 0.9,
        "counterexample": "" if p < 0.05 and abs(r) >= 0.9 else f"r={r}, p={p}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(3, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_r = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_r = math.sqrt(sum((r["metric_value"] - mean_r) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")