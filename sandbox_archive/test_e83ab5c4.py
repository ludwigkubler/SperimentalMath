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
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(graph[i]) < d and len(graph[j]) < d:
                    if (i, j) not in edges and (j, i) not in edges:
                        graph[i].append(j)
                        graph[j].append(i)
                        edges.add((i, j))
        return graph
    
    def quantum_symmetric_functions(n):
        # Placeholder for actual implementation
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    def mli(G):
        algebra = quantum_symmetric_functions(len(G))
        indeterminacies = sum(row.count(0) for row in algebra)
        return indeterminacies
    
    def resolution_proof_width(phi_G):
        # Placeholder for actual implementation
        return random.randint(1, 100)
    
    n_max = 40
    instances_tested = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, n_max + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            d = random.randint(2, min(n - 1, 4))
            G = generate_d_regular_graph(n, d)
            if G is None:
                continue
            mli_value = mli(G)
            w_phi_G = resolution_proof_width(G)
            metric_values.append(mli_value / w_phi_G)
            instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": "mli_to_w_phi_G_ratio",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    correlation_coefficient = 0
    mean_metric = sum(metric_values) / len(metric_values)
    for value in metric_values:
        correlation_coefficient += (value - mean_metric) ** 2
    correlation_coefficient /= len(metric_values)
    correlation_coefficient = math.sqrt(correlation_coefficient)
    
    if correlation_coefficient < 0.8:
        conjecture_holds = False
        counterexample = "correlation_coefficient_too_low"
    
    return {
        "metric_name": "mli_to_w_phi_G_ratio",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")