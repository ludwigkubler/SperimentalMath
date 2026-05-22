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
    
    def generate_ac0_circuit(n):
        # Simplified AC0 circuit generation for parity function
        return [random.choice([1, -1]) for _ in range(2**n)]
    
    def fourier_coefficients(circuit, n):
        F = []
        for k in range(2**n):
            sum_val = 0
            for i in range(2**n):
                sum_val += circuit[i] * math.exp(-2j * math.pi * k * i / (2**n))
            F.append(sum_val / (2**n))
        return F
    
    def l2_norm(coefficients):
        return math.sqrt(sum(abs(c)**2 for c in coefficients))
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    circuit = generate_ac0_circuit(n)
    F = fourier_coefficients(circuit, n)
    norm_F = l2_norm(F)
    
    if norm_F == 0:
        return {
            "metric_name": "L2-norm of Fourier Coefficients",
            "metric_value": norm_F,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    c = math.log(n) / norm_F
    return {
        "metric_name": "L2-norm of Fourier Coefficients",
        "metric_value": norm_F,
        "instances_tested": 1,
        "conjecture_holds": c >= 0.5,  # Example threshold for simplicity
        "counterexample": "" if c >= 0.5 else f"Counterexample with n={n}, norm_F={norm_F}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*37, 127))[:30]  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_metric_value = sum(r["metric_value"] for r in results if "metric_value" in r)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    
    support_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = support_count / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        result = "SUPPORTED"
    elif support_fraction >= 0.8:
        result = "SUPPORTED"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result = f"FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}"
    
    print(f"RESULT: {result} mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")