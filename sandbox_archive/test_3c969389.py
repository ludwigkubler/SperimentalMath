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
    
    def generate_circuit(depth):
        if depth == 1:
            return [random.choice([0, 1])]
        else:
            sub_depth = random.randint(1, depth - 1)
            left = generate_circuit(sub_depth)
            right = generate_circuit(depth - sub_depth)
            gate = random.choice(['AND', 'OR'])
            return [gate] + left + right
    
    def count_connected_components(circuit):
        if not circuit:
            return 0
        stack = [circuit]
        visited = set()
        components = 0
        
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                if isinstance(node, list):
                    for child in node[1:]:
                        stack.append(child)
                else:
                    components += 1
        return components
    
    def calculate_correlation(circuits, depths):
        if len(circuits) != len(depths):
            raise ValueError("Circuits and depths must have the same length")
        
        n = len(circuits)
        sum_depth = sum(depths)
        sum_components = sum(count_connected_components(circuit) for circuit in circuits)
        sum_depth_squared = sum(d ** 2 for d in depths)
        sum_depth_components = sum(d * count_connected_components(circuit) for d, circuit in zip(depths, circuits))
        
        mean_depth = sum_depth / n
        mean_components = sum_components / n
        
        numerator = n * sum_depth_components - sum_depth * mean_components
        denominator = math.sqrt((n * sum_depth_squared - sum_depth ** 2) * (n * sum_components ** 2 - sum_components ** 2))
        
        if denominator == 0:
            return None
        
        correlation_coefficient = numerator / denominator
        return correlation_coefficient
    
    n_max = 40
    instances_tested = 30
    depths = [random.randint(5, n_max) for _ in range(instances_tested)]
    circuits = [generate_circuit(d) for d in depths]
    
    components = [count_connected_components(circuit) for circuit in circuits]
    correlation_coefficient = calculate_correlation(components, depths)
    
    conjecture_holds = correlation_coefficient is not None and abs(correlation_coefficient - 1) < 0.05
    counterexample = "" if conjecture_holds else "correlation_coefficient_outside_margin"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_outside_margin\" first_failing_seed={first_failing_seed}")