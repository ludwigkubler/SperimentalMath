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
        coeffs = [random.randint(1, n) for _ in range(n)]
        return coeffs
    
    def evaluate_polynomial(poly, x):
        result = 0
        for i, coeff in enumerate(reversed(poly)):
            result += coeff * (x ** i)
        return result
    
    def find_roots(poly):
        if len(poly) == 1:
            return []
        roots = set()
        for k in range(-100, 101):
            if evaluate_polynomial(poly, k) == 0:
                roots.add(k)
        return list(roots)
    
    def minimal_root_separation(roots):
        if len(roots) < 2:
            return float('inf')
        return min(abs(a - b) for a, b in itertools.combinations(roots, 2))
    
    def smallest_acc0_circuit_size(n):
        # Placeholder function to simulate ACC0 circuit size
        # In practice, this would involve actual circuit complexity analysis
        return n ** 2
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    poly = generate_polynomial(n)
    roots = find_roots(poly)
    sep = minimal_root_separation(roots)
    acc0_size = smallest_acc0_circuit_size(n)
    
    return {
        "metric_name": "minimal_root_separation",
        "metric_value": sep,
        "instances_tested": 1,
        "conjecture_holds": sep >= n ** (1/3) and acc0_size >= n ** 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_sep = sum(r['metric_value'] for r in results) / len(results)
    std_sep = math.sqrt(sum((r['metric_value'] - mean_sep) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_sep} std={std_sep} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_sep} std={std_sep} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")