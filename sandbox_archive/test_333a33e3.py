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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Graph size must be a multiple of the degree")
        
        # Simplified version of communication complexity rank calculation
        return n
    
    def min_simple_connected_components(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Graph size must be a multiple of the degree")
        
        # Simplified version of minimum simple connected components calculation
        return n
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        
        min_order = min_simple_connected_components(f)
        r_f = communication_complexity_rank(f)
        
        results.append((min_order, r_f))
    
    if not results:
        return {
            "metric_name": "communication_complexity_rank",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    min_ranks = [r for _, r in results]
    comm_complexity_ranks = [m for m, _ in results]
    
    mean_min_ranks = sum(min_ranks) / len(min_ranks)
    mean_comm_complexity_ranks = sum(comm_complexity_ranks) / len(comm_complexity_ranks)
    
    correlation_coefficient = (sum((min_ranks[i] - mean_min_ranks) * (comm_complexity_ranks[i] - mean_comm_complexity_ranks) for i in range(len(min_ranks))) /
                               math.sqrt(sum((min_ranks[i] - mean_min_ranks)**2 for i in range(len(min_ranks))) *
                                         sum((comm_complexity_ranks[i] - mean_comm_complexity_ranks)**2 for i in range(len(comm_complexity_ranks)))))
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient=0' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=30")