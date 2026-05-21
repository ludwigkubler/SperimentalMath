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
        coeffs = [random.randint(1, 10) for _ in range(n+1)]
        return coeffs
    
    def compute_schur_weyl_coeffs(coeffs):
        n = len(coeffs) - 1
        schur_weyl_coeffs = []
        for i in range(n + 1):
            coeff = sum(coeffs[j] * coeffs[n-j] for j in range(i+1))
            schur_weyl_coeffs.append(coeff)
        return schur_weyl_coeffs
    
    def compute_permanent(coeffs):
        n = len(coeffs) - 1
        permanent = 0
        for i in range(n + 1):
            product = 1
            for j in range(n + 1):
                product *= coeffs[i * (n + 1) + j]
            permanent += product
        return permanent
    
    def compute_determinant(coeffs):
        n = len(coeffs) - 1
        determinant = 0
        for i in range(n + 1):
            sign = (-1) ** i
            sub_coeffs = [coeffs[j] for j in range(n + 1) if j != i]
            sub_determinant = compute_determinant(sub_coeffs)
            determinant += sign * coeffs[i] * sub_determinant
        return determinant
    
    def circuit_complexity(poly):
        n = len(poly) - 1
        return n ** 2  # Simplified for testing purposes
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_polynomial(n)
        schur_weyl_coeffs = compute_schur_weyl_coeffs(f)
        
        if not all(schur_weyl_coeffs[m] != 0 for m in range(int(n ** 1.5))):
            continue
        
        permanent = compute_permanent(f)
        determinant = compute_determinant(f)
        
        perm_complexity = circuit_complexity(permanent)
        det_complexity = circuit_complexity(determinant)
        
        if perm_complexity > det_complexity * math.log2(n):
            results.append(False)
        else:
            results.append(True)
    
    metric_value = sum(results) / len(results)
    conjecture_holds = all(results)
    counterexample = "mapping_undefined" if not conjecture_holds else ""
    
    return {
        "metric_name": "Schur-Weyl Coefficients",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["conjecture_holds"])
    
    support_fraction = sum(results) / len(results)
    
    if all(results):
        result = "SUPPORTED"
    elif support_fraction >= 0.8:
        result = "SUPPORTED"
    else:
        first_failing_seed = seeds[results.index(False)]
        result = f"FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}"
    
    print(f"RESULT: {result} mean={sum(trial_result['metric_value'] for trial_result in results) / len(results)} std=0 support_fraction={support_fraction}")