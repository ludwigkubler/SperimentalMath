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
    
    def generate_polynomial(n):
        coefficients = [random.randint(1, 10) for _ in range(n + 1)]
        return coefficients
    
    def evaluate_polynomial(poly, x):
        result = 0
        for i, coeff in enumerate(poly):
            result += coeff * (x ** i)
        return result
    
    def find_roots(poly):
        n = len(poly) - 1
        if n == 0:
            return []
        elif n == 1:
            return [-poly[0] / poly[1]]
        
        roots = []
        for i in range(n + 1):
            x = random.uniform(-10, 10)
            while abs(evaluate_polynomial(poly, x)) > 1e-6:
                x += random.uniform(-0.1, 0.1)
            roots.append(x)
        
        return roots
    
    def minimal_root_separation(roots):
        if len(roots) < 2:
            return float('inf')
        return min(abs(roots[i] - roots[j]) for i in range(len(roots)) for j in range(i + 1, len(roots)))
    
    def acc0_circuit_size(poly):
        n = len(poly) - 1
        if n == 0:
            return 1
        elif n == 1:
            return 2
        
        size = n * (n + 1) // 2
        for i in range(n + 1):
            size += abs(poly[i])
        
        return size
    
    def is_in_p(poly):
        # Placeholder function to check if a polynomial is in P
        return True
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        poly = generate_polynomial(n)
        if not is_in_p(poly):
            continue
        
        roots = find_roots(poly)
        min_separation = minimal_root_separation(roots)
        circuit_size = acc0_circuit_size(poly)
        
        results.append({
            "n": n,
            "min_separation": min_separation,
            "circuit_size": circuit_size
        })
    
    if not results:
        return {
            "metric_name": "minimal_root_separation",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid polynomials found"
        }
    
    min_separations = [result["min_separation"] for result in results]
    circuit_sizes = [result["circuit_size"] for result in results]
    
    mean_min_separation = sum(min_separations) / len(min_separations)
    std_min_separation = math.sqrt(sum((x - mean_min_separation) ** 2 for x in min_separations) / len(min_separations))
    mean_circuit_size = sum(circuit_sizes) / len(circuit_sizes)
    
    conjecture_holds = all(ms >= n**(1/3) and cs >= n**2 for ms, cs, n in zip(min_separations, circuit_sizes, n_values))
    counterexample = "" if conjecture_holds else "None found"
    
    return {
        "metric_name": "minimal_root_separation",
        "metric_value": mean_min_separation,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"None found\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")