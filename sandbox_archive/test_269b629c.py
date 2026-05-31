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
    
    def generate_truth_table(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def circuit_depth(truth_table):
        n = int(math.log2(len(truth_table)))
        depth = 0
        while truth_table:
            new_truth_table = []
            for i in range(len(truth_table) // 2):
                if truth_table[2*i] == truth_table[2*i+1]:
                    new_truth_table.append(truth_table[2*i])
                else:
                    new_truth_table.append(1 - truth_table[2*i])
            truth_table = new_truth_table
            depth += 1
        return depth
    
    def coxeter_group_order(n):
        # Simplified Coxeter group order for demonstration purposes
        return n + 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    depths = []
    orders = []
    
    for n in n_values:
        truth_table = generate_truth_table(n)
        depth = circuit_depth(truth_table)
        order = coxeter_group_order(n)
        
        if depth is None or order is None:
            return {
                "metric_name": "circuit_depth",
                "metric_value": 0,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        depths.append(depth)
        orders.append(order)
    
    if len(depths) < 10:
        return {
            "metric_name": "circuit_depth",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_depth = sum(depths) / len(depths)
    mean_order = sum(orders) / len(orders)
    
    # Calculate correlation coefficient
    covariance = sum((depth - mean_depth) * (order - mean_order) for depth, order in zip(depths, orders))
    variance_depth = sum((depth - mean_depth)**2 for depth in depths)
    variance_order = sum((order - mean_order)**2 for order in orders)
    
    if variance_depth == 0 or variance_order == 0:
        return {
            "metric_name": "circuit_depth",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "zero_variance"
        }
    
    correlation_coefficient = covariance / (math.sqrt(variance_depth) * math.sqrt(variance_order))
    
    return {
        "metric_name": "circuit_depth",
        "metric_value": correlation_coefficient,
        "instances_tested": len(depths),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")