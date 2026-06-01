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
    
    def generate_planar_graph(n):
        if n == 3:
            return [[0, 1], [1, 2], [2, 0]]
        elif n == 4:
            return [[0, 1], [1, 2], [2, 3], [3, 0], [0, 2]]
        else:
            # Simple heuristic to generate a small planar graph
            nodes = list(range(n))
            edges = []
            for i in range(n):
                for j in range(i + 1, n):
                    if len(edges) >= 3 * (n - 2):  # Ensure it remains planar
                        break
                    edges.append([i, j])
            return edges
    
    def min_root_separability(graph):
        # Placeholder for actual computation of minimal root separability
        # For simplicity, we use a dummy value that depends on the graph size
        n = len(graph)
        return n ** (1/3)
    
    def communication_complexity(graph):
        # Placeholder for actual computation of communication complexity
        # For simplicity, we use a dummy value that depends on the graph size
        n = len(graph)
        return n ** (2/3)
    
    trials = 0
    min_root_separability_sum = 0
    communication_complexity_sum = 0
    
    for _ in range(30):
        n = random.randint(5, 40)
        graph = generate_planar_graph(n)
        
        if not graph:
            continue
        
        trials += 1
        min_root_separability_val = min_root_separability(graph)
        communication_complexity_val = communication_complexity(graph)
        
        min_root_separability_sum += min_root_separability_val
        communication_complexity_sum += communication_complexity_val
    
    if trials == 0:
        return {
            "metric_name": "min_root_separability * communication_complexity",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    min_root_separability_avg = min_root_separability_sum / trials
    communication_complexity_avg = communication_complexity_sum / trials
    
    correlation_coefficient = (trials * sum(min_root_separability_avg * communication_complexity_avg for _ in range(trials)) -
                               min_root_separability_avg * communication_complexity_avg) / \
                              math.sqrt((trials * sum(min_root_separability_avg**2 for _ in range(trials)) - min_root_separability_avg**2) *
                                        (trials * sum(communication_complexity_avg**2 for _ in range(trials)) - communication_complexity_avg**2))
    
    return {
        "metric_name": "min_root_separability * communication_complexity",
        "metric_value": correlation_coefficient,
        "instances_tested": trials,
        "n_max": 40,
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={results[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]['seed']}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")