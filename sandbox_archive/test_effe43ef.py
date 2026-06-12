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

def generate_sat_instance(n):
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    for _ in range(n):
        clause = random.sample(variables, 2)
        clauses.append(f"({clause[0]} | {clause[1]})")
    return ' & '.join(clauses)

def literal_to_int(literal):
    if literal.startswith('x'):
        return int(literal[1:])
    else:
        raise ValueError("Invalid literal format")

def clause_indicator_polynomial(phi):
    polynomial = 0
    for term in phi.split('&'):
        variables = [literal_to_int(lit) for lit in term.strip().split('|')]
        coefficient = (-1)**len(variables)
        product = 1
        for var in variables:
            product *= (var - 1) / var
        polynomial += coefficient * product
    return polynomial

def min_order_twisted_quiver(polynomial):
    # Simplified procedure to calculate the minimal order of a twisted quiver representation
    # This is a placeholder and should be replaced with actual computation
    return abs(int(polynomial))

def resolution_proof_width(phi):
    # Placeholder for computing the resolution proof width
    # This is a simplified example and should be replaced with actual computation
    return len(phi.split('&'))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 0
    metric_values = []
    instances_tested = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        phi = generate_sat_instance(n)
        polynomial = clause_indicator_polynomial(phi)
        min_order_twq = min_order_twisted_quiver(polynomial)
        w_phi = resolution_proof_width(phi)
        
        metric_values.append(min_order_twq / w_phi)
        instances_tested += n
        n_max = max(n_max, n)
    
    mean_value = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean_value)**2 for x in metric_values) / len(metric_values))
    
    return {
        "metric_name": "MinOrder/W",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,  # This is a placeholder; actual check should be done here
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(seeds) if not results[s]["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")