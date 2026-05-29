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
    
    def fourier_coefficients(f):
        n = len(f)
        coeffs = []
        for k in range(n + 1):
            coeff = Fraction(0)
            for i in range(2**n):
                term = f[i] * (-1)**sum((i >> j) & 1 for j in range(k))
                coeff += term
            coeff /= 2**n
            coeffs.append(coeff)
        return coeffs
    
    def construct_octonion_algebra(coeffs):
        n = len(coeffs)
        O = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            for j in range(n + 1):
                if i == j:
                    O[i][j] = coeffs[i]
                else:
                    O[i][j] = Fraction(0)
        return O
    
    def minimal_order_of_center(O):
        n = len(O) - 1
        center = [O[i][i] for i in range(n + 1)]
        order = max(abs(coeff) for coeff in center)
        return int(math.ceil(order))
    
    def read_twice_bp_size(f):
        n = len(f)
        size = 0
        for i in range(2**n):
            for j in range(i, 2**n):
                if f[i] == f[j]:
                    size += 1
        return size
    
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.randint(5, 40)
        f = generate_boolean_function(n)
        coeffs = fourier_coefficients(f)
        O = construct_octonion_algebra(coeffs)
        ord_C_O = minimal_order_of_center(O)
        BP_rtw_f = read_twice_bp_size(f)
        results.append((ord_C_O, BP_rtw_f))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "no_data"
        }
    
    ord_C_Os, BP_rtw_fs = zip(*results)
    correlation = sum((ord_C_O - mean) * (BP_rtw_f - mean) for ord_C_O, BP_rtw_f in results) / len(results)
    mean = sum(ord_C_Os) / len(ord_C_Os)
    std = math.sqrt(sum((x - mean)**2 for x in ord_C_Os) / len(ord_C_Os))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "conjecture_holds": abs(correlation) > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_data")
    else:
        mean_corr = sum(result["metric_value"] for result in results) / len(results)
        std_corr = math.sqrt(sum((result["metric_value"] - mean_corr)**2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if abs(result["metric_value"]) > 0.7) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
        elif any(not result["conjecture_holds"] for result in results):
            first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"correlation_threshold_not_met\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE insufficient_support")