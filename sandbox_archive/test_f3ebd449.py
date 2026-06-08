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
    
    def generate_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(instance):
        n = len(instance)
        c = 0
        for i in range(n):
            if instance[i] != instance[(i + 1) % n]:
                c += 1
        return c
    
    def minimal_geometric_entropy(graph):
        n = len(graph)
        total_edges = sum(sum(row) for row in graph)
        max_degree = max(sum(row) for row in graph)
        mGE = (total_edges / (n * (n - 1))) * math.log2(max_degree + 1)
        return mGE
    
    def generate_graph(instance):
        n = len(instance)
        graph = [[0] * n for _ in range(n)]
        for i in range(n):
            if instance[i] != instance[(i + 1) % n]:
                graph[i][(i + 1) % n] = 1
                graph[(i + 1) % n][i] = 1
        return graph
    
    def calculate_metric(instance, c):
        graph = generate_graph(instance)
        mGE = minimal_geometric_entropy(graph)
        ratio = mGE / (c ** 2 * math.log(n, 2))
        return ratio
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_ratio = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            instance = generate_instance(n)
            c = communication_complexity(instance)
            if c == 0:  # Skip instances with zero complexity to avoid division by zero
                continue
            ratio = calculate_metric(instance, c)
            total_ratio += ratio
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_ratio = total_ratio / instances_tested
    support_fraction = (mean_ratio >= 0.9 and mean_ratio <= 1.1) * 100
    
    if support_fraction < 80:
        return {
            "metric_name": "mGE/c^2(log(n))",
            "metric_value": mean_ratio,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": f"mean_ratio={mean_ratio} (not within ±10% of 1)"
        }
    else:
        return {
            "metric_name": "mGE/c^2(log(n))",
            "metric_value": mean_ratio,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if 0.9 <= r["metric_value"] <= 1.1) / len(results) * 100
    
    if support_fraction >= 80:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=UNKNOWN support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] == False for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_ratio outside ±10% of 1\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=not_enough_support")