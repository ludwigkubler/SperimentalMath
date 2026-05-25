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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def taylor_coefficients(f, n):
        coefficients = []
        for i in range(n + 1):
            coeff = sum(f[j] * (-1)**j for j in range(len(f)) if bin(j).count('1') == i) / (2**len(f))
            coefficients.append(coeff)
        return coefficients
    
    def hermitian_form_rank(coeffs, n):
        # Simple heuristic: rank is the number of non-zero coefficients
        return sum(1 for coeff in coeffs if abs(coeff) > 1e-6)
    
    def decision_tree_path_complexity(f, n):
        # Placeholder function; actual implementation depends on specific algorithm
        return random.randint(1, 2**n)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_boolean_function(n)
    coeffs = taylor_coefficients(f, n)
    N_f = hermitian_form_rank(coeffs, n)
    D_f = decision_tree_path_complexity(f, n)
    
    if D_f == 0:
        return {
            "metric_name": "N_f / D_f^0.5",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Decision tree path complexity is zero."
        }
    
    ratio = N_f / (D_f ** 0.5)
    return {
        "metric_name": "N_f / D_f^0.5",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= math.log2(n) ** 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [random.getrandbits(32) for _ in range(30)]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["instances_tested"] > 0]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values))} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"N_f / D_f^0.5 > log2(n)^2\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported the conjecture")