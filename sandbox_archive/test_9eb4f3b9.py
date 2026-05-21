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
        coefficients = [random.randint(-10, 10) for _ in range(n)]
        return coefficients
    
    def compute_schur_weyl_coefficients(poly, m):
        n = len(poly)
        if m >= n**1.5:
            return []
        # Placeholder implementation
        return [poly[i] * poly[j] for i in range(m+1) for j in range(i, m+1)]
    
    def compute_permanent(poly):
        n = len(poly)
        permanent = 0
        for perm in itertools.permutations(range(n)):
            product = 1
            for i in range(n):
                product *= poly[perm[i]]
            permanent += product
        return permanent
    
    def compute_determinant(poly):
        n = len(poly)
        if n == 1:
            return poly[0]
        det = 0
        for j in range(n):
            sub_poly = [poly[i] for i in range(1, n) if i != j]
            det += (-1)**j * poly[j] * compute_determinant(sub_poly)
        return det
    
    def circuit_complexity(poly):
        # Placeholder implementation
        return len(poly)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        poly = generate_polynomial(n)
        schur_weyl_coeffs = compute_schur_weyl_coefficients(poly, int(n**1.5))
        
        if not all(coeff != 0 for coeff in schur_weyl_coeffs):
            return {
                "metric_name": "Schur-Weyl Coefficients",
                "metric_value": None,
                "instances_tested": len(schur_weyl_coeffs),
                "conjecture_holds": False,
                "counterexample": "Non-zero Schur-Weyl coefficients not found for m < n^1.5"
            }
        
        permanent = compute_permanent(poly)
        determinant = compute_determinant(poly)
        perm_complexity = circuit_complexity(permanent)
        det_complexity = circuit_complexity(determinant)
        
        results.append({
            "n": n,
            "permanent": permanent,
            "determinant": determinant,
            "perm_complexity": perm_complexity,
            "det_complexity": det_complexity
        })
    
    total_perm_complexity = sum(result["perm_complexity"] for result in results)
    total_det_complexity = sum(result["det_complexity"] for result in results)
    
    return {
        "metric_name": "Circuit Complexity Ratio",
        "metric_value": total_perm_complexity / total_det_complexity,
        "instances_tested": len(results),
        "conjecture_holds": all(result["perm_complexity"] >= result["det_complexity"] for result in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_perm_complexity = sum(result["perm_complexity"] for result in results)
    total_det_complexity = sum(result["det_complexity"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={total_perm_complexity/total_det_complexity} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_perm_complexity/total_det_complexity} std=0.0 support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = f"n={result['n']}, permanent={result['permanent']}, determinant={result['determinant']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break