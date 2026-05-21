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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_polynomial(n):
        coefficients = [random.randint(1, 10) for _ in range(n + 1)]
        return coefficients
    
    def compute_schur_weyl_coeffs(poly, n):
        # Placeholder for actual Schur-Weyl coefficient computation
        schur_weyl_coeffs = [0] * (n + 1)
        schur_weyl_coeffs[0] = poly[0]
        for k in range(1, n + 1):
            schur_weyl_coeffs[k] = sum(poly[i] * schur_weyl_coeffs[k - i] for i in range(k))
        return schur_weyl_coeffs
    
    def compute_permanent(poly, n):
        permanent = 0
        for perm in itertools.permutations(range(n)):
            product = 1
            for i in range(n):
                product *= poly[perm[i]]
            permanent += product
        return permanent
    
    def compute_determinant(poly, n):
        if n == 1:
            return poly[0]
        det = 0
        for j in range(n):
            sub_poly = [poly[j + 1] for j in range(j) + range(j + 2, n)]
            sub_det = compute_determinant(sub_poly, n - 1)
            if j % 2 == 0:
                det += poly[j] * sub_det
            else:
                det -= poly[j] * sub_det
        return det
    
    def circuit_complexity(poly):
        # Placeholder for actual circuit complexity computation
        return len(poly) ** 2
    
    n = random.randint(5, 40)
    poly = generate_polynomial(n)
    schur_weyl_coeffs = compute_schur_weyl_coeffs(poly, n)
    
    if not all(schur_weyl_coeffs[m] != 0 for m in range(int(n ** 1.5))):
        return {
            "metric_name": "circuit_complexity",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Schur-Weyl coefficients are zero for some m"
        }
    
    permanent = compute_permanent(poly, n)
    determinant = compute_determinant(poly, n)
    perm_complexity = circuit_complexity(permanent)
    det_complexity = circuit_complexity(determinant)
    
    return {
        "metric_name": "circuit_complexity",
        "metric_value": perm_complexity / det_complexity,
        "instances_tested": 1,
        "conjecture_holds": perm_complexity >= det_complexity * Fraction(1, 2),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Schur-Weyl coefficients are zero for some m' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")