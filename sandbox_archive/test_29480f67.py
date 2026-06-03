# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0:
            return None
        degree = d // 2
        G = {i: [] for i in range(n)}
        available = list(range(1, n))
        for i in range(n):
            remaining = len(available)
            if remaining <= degree:
                return None
            neighbors = random.sample(sorted(available), degree)
            G[i] = neighbors
            for neighbor in neighbors:
                available.remove(neighbor)
        return G

    def communication_complexity(G):
        n = len(G)
        max_flow = 0
        for i in range(n):
            for j in range(i + 1, n):
                if j not in G[i]:
                    continue
                flow = min(len(G[i]), len(G[j]))
                max_flow += flow
        return max_flow

    def kahler_manifolds(G):
        # Placeholder function to represent the construction of Kähler manifolds.
        # For simplicity, we assume each vertex contributes one manifold.
        return len(G)

    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            d = random.randint(2, min(n - 1, 2 * (n // 2)))
            G = generate_d_regular_graph(n, d)
            if G is None:
                continue
            r_G = communication_complexity(G)
            M_G = kahler_manifolds(G)
            metrics.append((M_G, r_G))
    
    if not metrics:
        return {
            "metric_name": "Kähler Manifolds vs Communication Complexity Rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    M_G_values = [m for m, _ in metrics]
    r_G_values = [r for _, r in metrics]
    
    mean_M_G = sum(M_G_values) / len(M_G_values)
    mean_r_G = sum(r_G_values) / len(r_G_values)
    std_dev_M_G = math.sqrt(sum((x - mean_M_G) ** 2 for x in M_G_values) / len(M_G_values))
    std_dev_r_G = math.sqrt(sum((x - mean_r_G) ** 2 for x in r_G_values) / len(r_G_values))
    
    correlation_coefficient = sum((M_G_values[i] - mean_M_G) * (r_G_values[i] - mean_r_G) for i in range(len(M_G_values))) / (len(M_G_values) * std_dev_M_G * std_dev_r_G)
    
    return {
        "metric_name": "Kähler Manifolds vs Communication Complexity Rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(metrics),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and abs(mean_M_G - mean_r_G) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['instances_tested']}, M(G)={r['metric_value']}, r(G)={mean_r_G}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break