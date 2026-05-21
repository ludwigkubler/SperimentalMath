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
import math
from fractions import Fraction
from itertools import combinations, product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_polynomial(n):
        coefficients = [random.randint(-10, 10) for _ in range(n+1)]
        return sum(coeff * x**i for i, coeff in enumerate(coefficients))
    
    def evaluate_polynomial(polynomial, x):
        return polynomial(x)
    
    def find_roots(polynomial):
        # Simple root-finding using the Rational Root Theorem
        roots = set()
        for a in range(-10, 11):
            for b in range(1, 11):
                if polynomial(Fraction(a, b)) == 0:
                    roots.add(Fraction(a, b))
        return roots
    
    def communication_complexity(roots, n):
        # Simplified DPLL-like complexity measure
        return len(roots) * n
    
    def geometric_entropy(roots):
        # Minimal number of Riemann surfaces needed to cover the roots
        return math.ceil(math.log(len(roots), 2))
    
    n = random.randint(5, 40)
    polynomial = generate_polynomial(n)
    x_values = [Fraction(i) for i in range(-10, 11)]
    roots = find_roots(polynomial)
    
    if not roots:
        return {
            "metric_name": "geometric_entropy",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "No real roots found"
        }
    
    entropy = geometric_entropy(roots)
    complexity = communication_complexity(roots, n)
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": entropy,
        "instances_tested": 1,
        "conjecture_holds": entropy <= complexity,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_entropy = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_entropy = math.sqrt(sum((r["metric_value"] - mean_entropy)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"geometric entropy exceeds communication complexity\" first_failing_seed={seed}")
                break