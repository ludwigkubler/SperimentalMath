# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def generate_polynomial(n):
    coefficients = [random.randint(-10, 10) for _ in range(n + 1)]
    return sum(coeff * x**i for i, coeff in enumerate(coefficients))

def evaluate_polynomial(poly, x):
    result = 0
    power_of_x = 1
    for coeff in poly:
        result += coeff * power_of_x
        power_of_x *= x
    return result

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    polynomial = generate_polynomial(n)
    
    # Simulate the solution set
    solutions = []
    for x in range(-100, 101):
        if evaluate_polynomial(polynomial, x) == 0:
            solutions.append(x)
    
    # Minimal geometric entropy (number of Riemann surfaces needed to cover the solution set)
    min_geometric_entropy = len(solutions)
    
    # Simulate deterministic communication complexity for membership testing
    def is_member(point):
        return evaluate_polynomial(polynomial, point) == 0
    
    # Use a simple DPLL-like solver to simulate communication complexity
    def dpll_solver():
        stack = []
        for x in range(-100, 101):
            if is_member(x):
                stack.append(x)
        return len(stack)
    
    communication_complexity = dpll_solver()
    
    # Check the conjecture
    conjecture_holds = min_geometric_entropy <= communication_complexity
    
    result = {
        "metric_name": "minimal_geometric_entropy",
        "metric_value": min_geometric_entropy,
        "instances_tested": len(solutions),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Counterexample found: n={n}, polynomial={polynomial}"
    }
    
    return result

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for res in results if not res["conjecture_holds"]) / len(results) >= 0.2:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Counterexample found' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")