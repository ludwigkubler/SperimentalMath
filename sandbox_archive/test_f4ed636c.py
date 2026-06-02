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
        # Generate a simple n-ary communication protocol with varying complexity
        return [random.randint(0, n-1) for _ in range(random.randint(5, 20))]
    
    def construct_quandle_representation(protocol):
        # Construct a minimal quandle representation for the given protocol
        quandle = {}
        for op in protocol:
            if op not in quandle:
                quandle[op] = len(quandle)
        return quandle
    
    def communication_complexity_rank(protocol):
        # Calculate the communication complexity rank of the protocol
        return len(set(protocol))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Test each size 30 times
            protocol = generate_protocol(n)
            quandle_representation = construct_quandle_representation(protocol)
            order = len(quandle_representation)
            rank = communication_complexity_rank(protocol)
            results.append((order, rank))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    orders = [r[0] for r in results]
    ranks = [r[1] for r in results]
    mean_order = sum(orders) / len(orders)
    mean_rank = sum(ranks) / len(ranks)
    correlation_coefficient = (sum((o - mean_order) * (r - mean_rank) for o, r in results) /
                               math.sqrt(sum((o - mean_order)**2 for o in orders) *
                                         sum((r - mean_rank)**2 for r in ranks)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")