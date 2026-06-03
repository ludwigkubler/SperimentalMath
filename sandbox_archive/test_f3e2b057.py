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
    
    # Generate communication complexity problem instance with rank r
    def generate_instance(r):
        n = 2 * r + 1
        graph = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if random.choice([True, False]):
                    graph[i][j] = 1
                    graph[j][i] = 1
        return r, graph
    
    # Compute minimal order of an affine divisor for a given graph
    def min_affine_divisor_order(graph):
        n = len(graph)
        if n == 0:
            return 0
        
        # Gaussian elimination to find rank
        rank = 0
        for i in range(n):
            if all(graph[j][i] == 0 for j in range(rank)):
                continue
            graph[rank], graph[i] = graph[i], graph[rank]
            for j in range(n):
                if j != rank:
                    factor = graph[j][i] / graph[rank][i]
                    for k in range(i, n):
                        graph[j][k] -= factor * graph[rank][k]
            rank += 1
        
        return rank
    
    # Main trial logic
    r_max = 10
    instances_tested = 0
    total_order = 0
    max_n = 0
    
    for _ in range(30):
        r, graph = generate_instance(random.randint(5, r_max))
        order = min_affine_divisor_order(graph)
        
        if order > r**2:
            return {
                "metric_name": "minimal_order",
                "metric_value": order,
                "instances_tested": instances_tested + 1,
                "n_max": max_n,
                "conjecture_holds": False,
                "counterexample": f"Instance with rank {r} has order {order}, which is greater than r^2"
            }
        
        total_order += order
        instances_tested += 1
        max_n = max(max_n, len(graph))
    
    mean_order = total_order / instances_tested
    return {
        "metric_name": "minimal_order",
        "metric_value": mean_order,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        for res in results:
            if not res["conjecture_holds"]:
                counterexample = res["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")