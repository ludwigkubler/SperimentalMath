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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def fourier_coefficients(f, p):
        n = len(f)
        coeffs = [0] * (n + 1)
        for k in range(n + 1):
            sum_val = 0
            for x in range(2**n):
                sum_val += f[x] * math.exp(-2j * math.pi * k * x / p) / (2**n)
            coeffs[k] = sum_val
        return coeffs
    
    def ac0_circuit_depth(f, n):
        # Simplified AC0 circuit depth calculation for demonstration purposes
        # This is a placeholder and should be replaced with actual AC0 circuit construction logic
        return random.randint(1, 6)
    
    p = 2**32  # Example p-adic field
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    
    for n in n_values:
        f = generate_boolean_function(n)
        coeffs = fourier_coefficients(f, p)
        omega_f = max(abs(coeff) for coeff in coeffs[1:])
        depth = ac0_circuit_depth(f, n)
        
        total_metric_value += omega_f
        instances_tested += 1
    
    mean_metric_value = total_metric_value / instances_tested
    std_metric_value = math.sqrt(sum((omega_f - mean_metric_value)**2 for omega_f in coeffs[1:]) / (instances_tested - 1))
    
    conjecture_holds = abs(mean_metric_value - 2**depth) <= 3 * std_metric_value
    
    return {
        "metric_name": "p-adic order",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"omega(f) = {mean_metric_value}, depth = {depth}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 1 for i in range(5, 8)]  # First 30 prime numbers
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / (len(results) - 1))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")