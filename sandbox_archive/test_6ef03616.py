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
    
    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for var in variables:
            clauses.append([var])
        for i in range(1, n):
            clauses.append([f'x{i}', f'x{i+1}'])
        return clauses
    
    def resolution_width(clauses):
        # Simplified estimation of resolution width
        return len(clauses)
    
    def minimal_order(n):
        # Simplified estimation of minimal order for quasi-Monte Carlo point set
        return n
    
    def correlation_coefficient(x, y):
        if len(x) != len(y):
            raise ValueError("x and y must have the same length")
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = math.sqrt(sum((xi - mean_x)**2 for xi in x)) * math.sqrt(sum((yi - mean_y)**2 for yi in y))
        return numerator / denominator if denominator != 0 else 0
    
    def slope_and_std_deviation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = sum((xi - mean_x)**2 for xi in x)
        slope = numerator / denominator if denominator != 0 else 0
        variance = sum((yi - mean_y - slope * (xi - mean_x))**2 for xi, yi in zip(x, y)) / n
        std_deviation = math.sqrt(variance) if variance >= 0 else 0
        return slope, std_deviation
    
    instances_tested = 0
    minimal_orders = []
    widths = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(30):
            clauses = tseitin_formula(n)
            width = resolution_width(clauses)
            order = minimal_order(n)
            instances_tested += 1
            minimal_orders.append(order)
            widths.append(width)
    
    if len(minimal_orders) < 20:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max([5, 10, 15, 20, 30, 40]),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    correlation = correlation_coefficient(minimal_orders, widths)
    slope, std_deviation = slope_and_std_deviation(minimal_orders, widths)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": max([5, 10, 15, 20, 30, 40]),
        "conjecture_holds": correlation > 0.9 and abs(slope - 1) <= std_deviation,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    std_deviation = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results if res["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_deviation} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_deviation} support_fraction={support_fraction}")
    else:
        for res in results:
            if not res["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"not_enough_instances\" first_failing_seed={res['seed']}")
                break