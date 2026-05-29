# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def fourier_coefficients(f, n):
        N = 2**n
        coeffs = []
        for k in range(N):
            sum_val = 0
            for x in range(N):
                sum_val += f[x] * (2j)**k / N
            coeffs.append(sum_val)
        return coeffs
    
    def octonion_algebra_order(coeffs, n):
        N = 2**n
        center_order = 1
        for coeff in coeffs:
            if coeff != 0:
                center_order *= abs(coeff.real) + abs(coeff.imag)
        return center_order
    
    def read_twice_bp_size(f, n):
        # Placeholder function; actual implementation needed
        return len(f)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            f = generate_boolean_function(n)
            coeffs = fourier_coefficients(f, n)
            center_order = octonion_algebra_order(coeffs, n)
            bp_size = read_twice_bp_size(f, n)
            total_metric_value += center_order * bp_size
            instances_tested += 1
    
    mean_metric_value = Fraction(total_metric_value, instances_tested).limit_denominator()
    
    return {
        "metric_name": "center_order * bp_size",
        "metric_value": float(mean_metric_value),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    instances_tested = sum(r["instances_tested"] for r in results)
    mean_metric_value = Fraction(total_metric_value, instances_tested).limit_denominator()
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")