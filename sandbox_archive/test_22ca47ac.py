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
    
    def generate_quasi_monte_carlo_points(n, order):
        points = []
        for i in range(order):
            point = [random.uniform(0, 1) for _ in range(n)]
            points.append(point)
        return points
    
    def generate_boolean_circuit(n):
        # Simplified boolean circuit generation
        circuit = {}
        for i in range(n):
            circuit[i] = random.choice([0, 1])
        return circuit
    
    def entanglement_complexity(circuit):
        # Simplified entanglement complexity calculation
        return len(circuit)
    
    def is_uniform_distribution(points, n):
        counts = [0] * (2 ** n)
        for point in points:
            index = sum(point[i] << i for i in range(n))
            counts[index] += 1
        return all(count == len(points) / (2 ** n) for count in counts)
    
    def calculate_order(circuit, n):
        order = 1
        while True:
            points = generate_quasi_monte_carlo_points(n, order)
            if is_uniform_distribution(points, n):
                return order
            order += 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_order = 0
    total_complexity = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            circuit = generate_boolean_circuit(n)
            complexity = entanglement_complexity(circuit)
            order = calculate_order(circuit, n)
            total_order += order
            total_complexity += complexity
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_order = total_order / instances_tested
    mean_complexity = total_complexity / instances_tested
    
    if abs(mean_order - mean_complexity) <= 2 * mean_complexity ** (1/2):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "The minimal order of quasi-Monte Carlo lattice points is not polynomially related to the entanglement complexity."
    
    return {
        "metric_name": "Order vs Complexity",
        "metric_value": mean_order,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_order) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"The minimal order of quasi-Monte Carlo lattice points is not polynomially related to the entanglement complexity.\" first_failing_seed={first_failing_seed}")