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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = len(f)
        ranks = []
        for i in range(2**n):
            rank = 0
            for j in range(2**n):
                if f[i] == f[j]:
                    rank += 1
            ranks.append(rank)
        return sum(ranks) / (2**n * n)
    
    def brauer_group_order(f):
        # Placeholder for Brauer group order calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(f)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        order = brauer_group_order(f)
        rank = communication_complexity_rank(f)
        results.append((order, rank))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    orders = [r[0] for r in results]
    ranks = [r[1] for r in results]
    mean_order = sum(orders) / len(orders)
    mean_rank = sum(ranks) / len(ranks)
    variance_rank = sum((x - mean_rank)**2 for x in ranks) / len(ranks)
    
    correlation = (sum((orders[i] - mean_order) * (ranks[i] - mean_rank) for i in range(len(orders))) /
                   math.sqrt(sum((orders[i] - mean_order)**2 for i in range(len(orders))) *
                             sum((ranks[i] - mean_rank)**2 for i in range(len(ranks)))))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) >= 0.8 and len(results) >= 24,
        "counterexample": "" if abs(correlation) >= 0.8 else "correlation < 0.8"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")