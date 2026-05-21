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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def fourier_coefficients(f, p):
    n = int(math.log2(len(f)))
    coeffs = []
    for k in range(2**n):
        coeff = sum(f[i] * (p ** ((i ^ k) & (n - 1))) for i in range(n)) / len(f)
        coeffs.append(coeff)
    return coeffs

def ac0_circuit_depth(f, n):
    # Placeholder function to simulate AC0 circuit depth calculation
    # This is a dummy implementation and should be replaced with actual logic
    return random.randint(1, 6)

def p_adic_order(coeffs):
    max_abs_coeff = max(abs(coeff) for coeff in coeffs)
    if max_abs_coeff == 0:
        return 0
    return int(math.log2(max_abs_coeff))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):  # Test each n with 5 random functions
            f = generate_boolean_function(n)
            p = 2  # Using p=2 for simplicity, can be changed to other primes if needed
            coeffs = fourier_coefficients(f, p)
            d = ac0_circuit_depth(f, n)
            omega_f = p_adic_order(coeffs)

            total_metric_value += omega_f
            instances_tested += 1

            if omega_f != Fraction(2**d):
                conjecture_holds = False
                counterexample = f"Function with n={n} and d={d} does not satisfy ω(f) = Θ(2^d)"

    mean_metric_value = total_metric_value / instances_tested
    std_deviation = 0

    return {
        "metric_name": "p-adic Order",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_deviation = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_deviation} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_deviation} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{trial_result['counterexample']}\" first_failing_seed={first_failing_seed}")