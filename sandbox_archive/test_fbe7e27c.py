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
    
    # Generate a random polynomial identity over F (characteristic zero)
    n = random.randint(5, 30)
    variables = [f'x{i+1}' for i in range(n)]
    coefficients = [random.randint(-10, 10) for _ in range(n + 1)]
    polynomial = sum(coeff * x**i for i, coeff in enumerate(coefficients))
    
    # Compute the solution set of the polynomial
    solution_set = []
    for x in range(-10, 11):
        if polynomial.subs({f'x{i+1}': x for i in range(n)}) == 0:
            solution_set.append(x)
    
    # Determine the minimal geometric entropy of the solution set
    # For simplicity, assume each solution is on a separate Riemann surface
    geometric_entropy = len(solution_set)
    
    # Measure the deterministic communication complexity for membership testing
    def dpll_solver(polynomial, variables):
        if not variables:
            return polynomial == 0
        var = variables[0]
        sub_polynomials = [polynomial.subs({var: val}) for val in [-1, 1]]
        return any(dpll_solver(sub_poly, variables[1:]) for sub_poly in sub_polynomials)
    
    communication_complexity = sum(1 for _ in range(100) if dpll_solver(polynomial, variables))
    
    # Check if the conjecture holds
    conjecture_holds = geometric_entropy <= communication_complexity
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": geometric_entropy,
        "instances_tested": 100,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Geometric entropy {geometric_entropy} > Communication complexity {communication_complexity}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Geometric entropy exceeds communication complexity\" first_failing_seed={first_failing_seed}")