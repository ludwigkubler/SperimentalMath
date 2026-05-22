# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_polynomial(degree):
        coeffs = [random.randint(0, 10) for _ in range(degree + 1)]
        return coeffs
    
    def evaluate_polynomial(poly, x):
        result = 0
        for i, coeff in enumerate(reversed(poly)):
            result += coeff * (x ** i)
        return result
    
    def min_root_separation(poly):
        roots = []
        degree = len(poly) - 1
        if degree == 0:
            return float('inf')
        elif degree == 1:
            root = -poly[0] / poly[1]
            roots.append(root)
        else:
            for i in range(degree + 1):
                x = Fraction(i, degree)
                value = evaluate_polynomial(poly, x)
                if value == 0:
                    roots.append(x)
        return min(abs(r1 - r2) for r1, r2 in itertools.combinations(roots, 2)) if roots else float('inf')
    
    def construct_ac0_circuit(poly):
        # This is a placeholder function. In practice, constructing an AC0 circuit
        # would be complex and beyond the scope of this test.
        return len(poly) * 10
    
    degree = random.randint(5, 40)
    poly = generate_polynomial(degree)
    
    min_separation = min_root_separation(poly)
    ac0_circuit_size = construct_ac0_circuit(poly)
    
    if min_separation == float('inf'):
        return {
            "metric_name": "min_root_separation",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "No distinct roots found"
        }
    
    return {
        "metric_name": "min_root_separation",
        "metric_value": min_separation,
        "instances_tested": 1,
        "conjecture_holds": ac0_circuit_size >= degree ** 2,  # Placeholder condition
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")