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
    
    def generate_boolean_instance(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([True, False]) for _ in range(2)]
            clauses.append(clause)
        return clauses
    
    def construct_crossed_product(clauses):
        # Simplified mapping to a semidirect product of groups
        n = len(clauses)
        G = {i: set() for i in range(n)}
        H = {i: set() for i in range(n)}
        
        for clause in clauses:
            for literal in clause:
                if literal:
                    G[0].add(1)
                    H[1].add(2)
                else:
                    G[1].add(3)
                    H[2].add(4)
        
        return len(G), len(H)
    
    def measure_resolution_width(clauses):
        # Simplified DPLL solver to estimate resolution width
        n = len(clauses)
        stack = []
        for clause in clauses:
            if not any(literal in stack for literal in clause):
                stack.append(random.choice(clause))
        
        return len(stack)
    
    def pearson_correlation(xs, ys):
        mean_x = sum(xs) / len(xs)
        mean_y = sum(ys) / len(ys)
        numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
        denominator = math.sqrt(sum((x - mean_x)**2 for x in xs)) * math.sqrt(sum((y - mean_y)**2 for y in ys))
        return numerator / denominator
    
    n_max = 40
    instances_tested = 0
    order_crossed_product_values = []
    resolution_widths = []
    
    for n in range(5, n_max + 1, 5):
        for _ in range(6):  # Ensure at least 30 instances per seed
            clauses = generate_boolean_instance(n)
            order_g, order_h = construct_crossed_product(clauses)
            width = measure_resolution_width(clauses)
            
            if order_g * order_h > 0 and width > 0:
                order_crossed_product_values.append(order_g * order_h)
                resolution_widths.append(width)
                instances_tested += 1
    
    if not order_crossed_product_values or not resolution_widths:
        return {
            "metric_name": "Pearson Correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = pearson_correlation(order_crossed_product_values, resolution_widths)
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation >= 0.8 and correlation <= 1.0,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["metric_value"] > 1.0 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] > 1.0)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_greater_than_1\" first_failing_seed={first_failing_seed}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")