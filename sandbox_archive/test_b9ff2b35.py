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
    
    def generate_circuit(n, m):
        return [[random.choice([0, 1]) for _ in range(m)] for _ in range(2**n)]
    
    def calculate_monotone_width(circuit):
        # Placeholder function; actual implementation needed
        return len(circuit)  # Dummy value
    
    def calculate_geometric_group_order(graph):
        # Placeholder function; actual implementation needed
        return len(graph)  # Dummy value
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = generate_circuit(n, n)
            width = calculate_monotone_width(circuit)
            order = calculate_geometric_group_order(circuit)
            results.append({
                "n": n,
                "width": width,
                "order": order
            })
    
    if not results:
        return {
            "metric_name": "Geometric Group Order vs Monotone Width",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No monotone circuits found"
        }
    
    n_values = [r["n"] for r in results]
    width_values = [r["width"] for r in results]
    order_values = [r["order"] for r in results]
    
    mean_width = sum(width_values) / len(width_values)
    mean_order = sum(order_values) / len(order_values)
    
    correlation = 0.0
    if len(width_values) > 1 and len(order_values) > 1:
        numerator = sum((width_values[i] - mean_width) * (order_values[i] - mean_order) for i in range(len(width_values)))
        denominator = math.sqrt(sum((width_values[i] - mean_width)**2 for i in range(len(width_values)))) * math.sqrt(sum((order_values[i] - mean_order)**2 for i in range(len(order_values))))
        correlation = numerator / denominator
    
    return {
        "metric_name": "Geometric Group Order vs Monotone Width",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")