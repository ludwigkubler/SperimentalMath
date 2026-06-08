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
    
    def truth_table_to_metric_space(truth_table):
        n = len(truth_table[0])
        metric_space = []
        for i in range(len(truth_table)):
            for j in range(i + 1, len(truth_table)):
                distance = sum(abs(a - b) for a, b in zip(truth_table[i], truth_table[j]))
                metric_space.append((i, j, distance))
        return metric_space
    
    def euclidean_distance(p1, p2):
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))
    
    def hyperbolic_distance(d):
        return math.log(1 + d)
    
    def communication_complexity(truth_table):
        n = len(truth_table[0])
        complexity = 0
        for i in range(n):
            for j in range(i + 1, n):
                if truth_table[i][j] != truth_table[j][i]:
                    complexity += 1
        return complexity
    
    def max_hyperbolic_distance(metric_space):
        distances = [d for _, _, d in metric_space]
        return max(distances)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        truth_table = [[random.randint(0, 1) for _ in range(n)] for _ in range(2 ** n)]
        metric_space = truth_table_to_metric_space(truth_table)
        max_dist = max_hyperbolic_distance(metric_space)
        comm_complexity = communication_complexity(truth_table)
        
        if comm_complexity == 0:
            continue
        
        results.append({
            "n": n,
            "max_dist": max_dist,
            "comm_complexity": comm_complexity
        })
    
    if not results:
        return {
            "metric_name": "communication_complexity",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    mean_comm_complexity = sum(res["comm_complexity"] for res in results) / len(results)
    max_dist_over_comm_complexity = max(res["max_dist"] / res["comm_complexity"] for res in results)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": max_dist_over_comm_complexity,
        "instances_tested": len(results),
        "n_max": max(res["n"] for res in results),
        "conjecture_holds": max_dist_over_comm_complexity >= 0.5,
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
    
    if all(res["conjecture_holds"] for res in results):
        mean_value = sum(res["metric_value"] for res in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        result = f"RESULT: FALSIFIED counterexample=\"max_dist_over_comm_complexity < 0.5\" first_failing_seed={first_failing_seed}"
    else:
        result = "RESULT: INCONCLUSIVE no_valid_instances"
    
    print(result)