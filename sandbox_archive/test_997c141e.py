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
    
    def communication_complexity(instance):
        n = len(instance)
        if n <= 1:
            return 0
        c = 0
        for i in range(n - 1):
            if instance[i] != instance[i + 1]:
                c += 1
        return c
    
    def minimal_geometric_entropy(G):
        n = len(G)
        degree_sum = sum(sum(1 for _ in neighbors) for _, neighbors in G.items())
        avg_degree = degree_sum / n
        mGE = (n * avg_degree - degree_sum ** 2 / (2 * n)) / math.log(n, 2)
        return mGE
    
    def generate_instance(n):
        instance = [random.choice([0, 1]) for _ in range(n)]
        return instance
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            instance = generate_instance(n)
            c = communication_complexity(instance)
            G = {i: [] for i in range(n)}
            for i in range(n - 1):
                if instance[i] != instance[i + 1]:
                    G[i].append(i + 1)
                    G[i + 1].append(i)
            
            mGE = minimal_geometric_entropy(G)
            ratio = mGE / (c ** 2 * math.log(n, 2))
            results.append({
                "n": n,
                "c": c,
                "mGE": mGE,
                "ratio": ratio
            })
    
    metric_value = sum(result["ratio"] for result in results) / len(results)
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    conjecture_holds = all(0.9 <= result["ratio"] <= 1.1 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Ratio of mGE to c^2(log(n))",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")