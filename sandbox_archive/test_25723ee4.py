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
        coeffs = [random.randint(1, 10) for _ in range(n + 1)]
        return coeffs
    
    def compute_schur_weyl_coeffs(coeffs):
        n = len(coeffs) - 1
        m = int(math.ceil(n ** 1.5))
        schur_weyl_coeffs = []
        for i in range(m):
            coeff = sum(coeffs[j] * coeffs[n-j] for j in range(i+1))
            schur_weyl_coeffs.append(coeff)
        return schur_weyl_coeffs
    
    def compute_permanent(coeffs):
        n = len(coeffs) - 1
        permanent = 0
        for i in range(n + 1):
            permanent += coeffs[i] * coeffs[n-i]
        return permanent
    
    def compute_determinant(coeffs):
        n = len(coeffs) - 1
        determinant = 0
        for i in range(n + 1):
            determinant += (-1)**i * coeffs[i] * coeffs[n-i]
        return determinant
    
    def circuit_complexity(value):
        if value == 0:
            return float('inf')
        return len(bin(abs(int(value)))) - 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_tests = 0
    supported_tests = 0
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            f = generate_polynomial(n)
            schur_weyl_coeffs = compute_schur_weyl_coeffs(f)
            permanent = compute_permanent(f)
            determinant = compute_determinant(f)
            
            if all(coeff != 0 for coeff in schur_weyl_coeffs):
                total_tests += 1
                perm_complexity = circuit_complexity(permanent)
                det_complexity = circuit_complexity(determinant)
                
                if perm_complexity > det_complexity * math.log(n, 2):
                    supported_tests += 1
                else:
                    counterexample = f"n={n}, permanent_complexity={perm_complexity}, determinant_complexity={det_complexity}"
    
    return {
        "metric_name": "circuit_complexity_ratio",
        "metric_value": supported_tests / total_tests if total_tests > 0 else float('nan'),
        "instances_tested": total_tests,
        "conjecture_holds": supported_tests >= 0.8 * total_tests,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    total_tests = sum(r["instances_tested"] for r in results if "instances_tested" in r)
    supported_tests = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = supported_tests / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=nan support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")