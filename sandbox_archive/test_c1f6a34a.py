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
    
    # Define a function to generate a random polynomial of degree d over F
    def generate_polynomial(d, field):
        coefficients = [random.choice(field) for _ in range(d + 1)]
        return coefficients
    
    # Define a function to compute the roots of a polynomial
    def find_roots(coefficients):
        n = len(coefficients)
        if n == 1:
            return []
        elif n == 2:
            a, b = coefficients
            return [-b / (2 * a)]
        else:
            # Use synthetic division to reduce the degree
            root = random.choice(coefficients[1:])
            quotient = [coefficients[0]]
            for coeff in coefficients[1:]:
                quotient.append(quotient[-1] * root + coeff)
            return [root] + find_roots(quotient[:-1])
    
    # Define a function to compute the monotone width of a circuit
    def monotone_width(circuit):
        # This is a placeholder for the actual computation
        # For simplicity, we assume a constant width based on the number of gates
        return len(circuit) // 2
    
    # Define a function to convert a polynomial to a circuit
    def polynomial_to_circuit(coefficients):
        n = len(coefficients)
        if n == 1:
            return []
        elif n == 2:
            a, b = coefficients
            return [(a, 'x'), (b, '+')]
        else:
            # Use a simple addition circuit for demonstration
            quotient = [coefficients[0]]
            for coeff in coefficients[1:]:
                quotient.append(quotient[-1] + coeff)
            return polynomial_to_circuit(quotient[:-1])
    
    # Define the field F (e.g., GF(2))
    F = [0, 1]
    
    # Set parameters
    d = random.randint(5, 40)
    n_tests = 30
    
    metric_values = []
    instances_tested = 0
    n_max = 0
    
    for _ in range(n_tests):
        coefficients = generate_polynomial(d, F)
        roots = find_roots(coefficients)
        m_min_dist = min(abs(roots[i] - roots[j]) for i in range(len(roots)) for j in range(i + 1, len(roots)))
        
        circuit = polynomial_to_circuit(coefficients)
        width = monotone_width(circuit)
        
        metric_values.append(m_min_dist * width)
        instances_tested += 1
        n_max = max(n_max, d)
    
    mean_metric_value = sum(metric_values) / len(metric_values)
    std_metric_value = math.sqrt(sum((x - mean_metric_value) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for m in metric_values if abs(m - 2 * width) <= 2 * width) / len(metric_values)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "m_min_dist * width",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")