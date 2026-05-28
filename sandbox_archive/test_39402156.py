# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_polynomial(degree):
        coefficients = [random.randint(-10, 10) for _ in range(degree + 1)]
        return coefficients
    
    def evaluate_polynomial(poly, x):
        return sum(c * (x ** i) for i, c in enumerate(poly))
    
    def find_diophantine_equation(poly):
        n = len(poly)
        for x in range(-100, 101):
            if evaluate_polynomial(poly, x) == 0:
                return x
        return None
    
    def order_of_equation(equation):
        return len(equation)
    
    D = 40
    instances_tested = 0
    total_order = 0
    conjecture_holds = True
    counterexample = ""
    
    for d in range(1, D + 1):
        for _ in range(30):  # Ensure at least 30 instances per degree
            poly = generate_polynomial(d)
            equation = find_diophantine_equation(poly)
            if equation is not None:
                order = order_of_equation(equation)
                total_order += order
                instances_tested += 1
                if order < Fraction(3 * d, 2):
                    conjecture_holds = False
                    counterexample = f"Degree {d}, Order {order}"
    
    mean_order = total_order / instances_tested if instances_tested > 0 else 0
    
    return {
        "metric_name": "Mean Order",
        "metric_value": mean_order,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results) if results else 0
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) if results else 0
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")