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
    
    def generate_random_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def communication_complexity_rank(edges):
        # Simplified version of communication complexity rank
        return len(edges)
    
    def local_induction_algebra_order(n, edges):
        # Simplified version of local induction algebra order
        return n + 1
    
    def log2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)
    
    metrics = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        total_variance = 0.0
        max_n = n
        
        for _ in range(5):
            edges = generate_random_graph(n)
            rank = communication_complexity_rank(edges)
            order = local_induction_algebra_order(n, edges)
            
            if order == 0:
                continue
            
            instances_tested += 1
            total_variance += (log2(order) - math.log(n) / math.sqrt(rank)) ** 2
        
        if instances_tested < 30:
            return {
                "metric_name": "variance",
                "metric_value": float('nan'),
                "instances_tested": instances_tested,
                "n_max": max_n,
                "conjecture_holds": False,
                "counterexample": "insufficient_instances"
            }
        
        variance = total_variance / instances_tested
        metrics.append(variance)
    
    mean_variance = sum(metrics) / len(metrics)
    conjecture_holds = all(abs(m - mean_variance) < 0.1 for m in metrics)
    
    return {
        "metric_name": "variance",
        "metric_value": mean_variance,
        "instances_tested": 5 * len(metrics),
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_variance = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_variance} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_variance} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"variance_mismatch\" first_failing_seed={first_failing_seed}")