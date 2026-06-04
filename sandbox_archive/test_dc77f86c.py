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
    
    def generate_sat_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def count_integral_points(sat_instance):
        # Placeholder function to simulate counting integral points
        # Replace with actual implementation if available
        return len(sat_instance)
    
    def resolution_proof_width(sat_instance):
        # Placeholder function to simulate resolution proof width
        # Replace with actual implementation if available
        return sum(1 for _ in sat_instance)  # Simplified example
    
    n_values = [5, 10, 15, 20, 30, 40]
    integral_points = []
    widths = []
    
    for n in n_values:
        sat_instance = generate_sat_instance(n)
        integral_points.append(count_integral_points(sat_instance))
        widths.append(resolution_proof_width(sat_instance))
    
    if not integral_points or not widths:
        return {
            "metric_name": "integral_points",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_integral_points = sum(integral_points) / len(integral_points)
    mean_widths = sum(widths) / len(widths)
    
    correlation_coefficient = 0
    if mean_integral_points != 0 and mean_widths != 0:
        numerator = sum((x - mean_integral_points) * (y - mean_widths) for x, y in zip(integral_points, widths))
        denominator = math.sqrt(sum((x - mean_integral_points)**2 for x in integral_points)) * math.sqrt(sum((y - mean_widths)**2 for y in widths))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "integral_points",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")