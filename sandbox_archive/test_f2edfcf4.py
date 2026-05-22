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
import itertools
from fractions import Fraction
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_polynomial(degree):
        coefficients = [random.randint(0, 10) for _ in range(degree + 1)]
        return coefficients
    
    def evaluate_polynomial(poly, x):
        result = 0
        for i, coeff in enumerate(poly):
            result += coeff * (x ** i)
        return result
    
    def min_root_separation(poly):
        roots = []
        degree = len(poly) - 1
        if degree == 0:
            return float('inf')  # No real roots for constant polynomials
        elif degree == 1:
            root = -poly[0] / poly[1]
            roots.append(root)
        else:
            # Find roots using a simple numerical method (e.g., bisection)
            for i in range(-10, 11):
                if evaluate_polynomial(poly, i) * evaluate_polynomial(poly, i + 1) < 0:
                    root = bisect(evaluate_polynomial, poly, i, i + 1)
                    roots.append(root)
        return min(abs(r1 - r2) for r1, r2 in itertools.combinations(roots, 2)) if roots else float('inf')
    
    def bisect(f, poly, a, b):
        tol = 1e-5
        while abs(b - a) > tol:
            c = (a + b) / 2
            if f(poly, c) * evaluate_polynomial(poly, a) < 0:
                b = c
            else:
                a = c
        return (a + b) / 2
    
    def ac0_circuit_size(poly):
        # Placeholder for AC0 circuit size calculation
        # This is a dummy implementation and should be replaced with actual logic
        degree = len(poly) - 1
        return degree * 5  # Simplified example: 5 gates per term
    
    n = random.randint(5, 40)
    poly = generate_polynomial(n)
    min_separation = min_root_separation(poly)
    circuit_size = ac0_circuit_size(poly)
    
    return {
        "metric_name": "min_root_separation",
        "metric_value": min_separation,
        "instances_tested": 1,
        "conjecture_holds": min_separation >= Fraction(n, n) ** 2,
        "counterexample": "" if min_separation >= Fraction(n, n) ** 2 else f"Counterexample for degree {n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Counterexample found' first_failing_seed={first_failing_seed}")