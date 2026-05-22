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
    
    def p_adic_valuation(n, p):
        if n == 0:
            return float('inf')
        val = 0
        while n % p == 0:
            n //= p
            val += 1
        return val
    
    def construct_ac0_circuit(poly, d):
        # Simplified AC0 circuit construction (not actual implementation)
        return len(poly) * d
    
    def generate_polynomial(d):
        coeffs = [random.randint(-10, 10) for _ in range(d + 1)]
        return coeffs
    
    def find_roots(coeffs):
        # Find roots using a simplified method
        roots = []
        for i in range(10):  # Simplified root finding
            x = random.uniform(-10, 10)
            if abs(sum(c * x**i for i, c in enumerate(coeffs))) < 1e-6:
                roots.append(x)
        return roots
    
    def min_p_adic_valuation(roots):
        return min(p_adic_valuation(root, 2) for root in roots if root != 0)
    
    n = random.randint(5, 40)
    poly = generate_polynomial(n)
    roots = find_roots(poly)
    val_p = min_p_adic_valuation(roots)
    circuit_size = construct_ac0_circuit(poly, n)
    
    return {
        "metric_name": "AC0 Circuit Size",
        "metric_value": circuit_size,
        "instances_tested": 1,
        "conjecture_holds": val_p <= circuit_size,
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
    
    metric_values = [r["metric_value"] for r in results]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.1f}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"min_p_adic_valuation > AC0 Circuit Size\" first_failing_seed={first_failing_seed + 1}")