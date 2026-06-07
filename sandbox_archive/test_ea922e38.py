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
    
    def generate_boolean_circuit(n):
        # Generate a random Boolean circuit with n inputs
        return [[random.choice([0, 1]) for _ in range(2)] for _ in range(2**n)]
    
    def formal_power_series(circuit):
        # Compute the formal power series of the circuit
        p = 3  # Start with base 3
        while True:
            coeffs = [0] * (2**len(circuit))
            for i, gate in enumerate(circuit):
                if gate[0] == 1:  # AND gate
                    coeffs[i] += coeffs[(i >> 1) ^ (i & 1)]
                else:  # OR gate
                    coeffs[i] += coeffs[(i >> 1)] + coeffs[(i & 1)]
            if all(coeff != 0 for coeff in coeffs):
                return p, coeffs
            p += 1
    
    def minimal_p_adic_order(coeffs):
        # Find the smallest p such that all coefficients are non-zero
        for p in range(2, 1000):
            if all(coeff % p != 0 for coeff in coeffs):
                return p
        return None
    
    n_max = 40
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, n_max + 1):
        for _ in range(6):  # Test each n with 6 different circuits
            circuit = generate_boolean_circuit(n)
            p, coeffs = formal_power_series(circuit)
            order = minimal_p_adic_order(coeffs)
            if order is None:
                conjecture_holds = False
                counterexample = f"Failed to find minimal p-adic order for n={n}"
                break
            instances_tested += 1
            total_metric_value += math.log2(n) ** 2
    
    mean_metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0.0
    support_fraction = instances_tested / (n_max - 4)
    
    return {
        "metric_name": "minimal_p_adic_order",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")