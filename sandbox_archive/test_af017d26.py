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
    
    def generate_protocol(n):
        # Generate a simple n-ary communication protocol
        return [random.randint(1, 2**n - 1) for _ in range(n)]
    
    def construct_quandle_representation(protocol):
        # Construct a minimal quandle representation (simplified example)
        quandle = {}
        for x in protocol:
            quandle[x] = {y: (x + y) % len(protocol) for y in protocol}
        return quandle
    
    def order_of_quandle(quandle):
        # Calculate the order of the quandle
        return max(len(quandle[x]) for x in quandle)
    
    def communication_complexity_rank(protocol):
        # Simplified example: rank is the number of unique elements
        return len(set(protocol))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        protocol = generate_protocol(n)
        quandle = construct_quandle_representation(protocol)
        order = order_of_quandle(quandle)
        rank = communication_complexity_rank(protocol)
        results.append((n, order, rank))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_values, orders, ranks = zip(*results)
    mean_order = sum(orders) / len(orders)
    mean_rank = sum(ranks) / len(ranks)
    correlation = (sum((x - mean_order) * (y - mean_rank) for x, y in zip(orders, ranks)) /
                   math.sqrt(sum((x - mean_order)**2 for x in orders) *
                             sum((y - mean_rank)**2 for y in ranks)))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67,
        71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        mean_value = None
        std_value = None
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(result['conjecture_holds'] for result in results) else 'FALSIFIED'} mean={mean_value} std={std_value} support_fraction={support_fraction}")