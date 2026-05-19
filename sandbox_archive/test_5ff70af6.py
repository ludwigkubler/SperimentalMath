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
    
    def fourier_transform(f, n):
        result = [0] * (1 << n)
        for i in range(1 << n):
            for j in range(n):
                if i & (1 << j):
                    result[i] += f[j]
                else:
                    result[i] -= f[j]
            result[i] /= 2 ** n
        return result
    
    def is_acc0_circuit(f, n, size_limit):
        # Placeholder for ACC0 circuit simulation logic
        # For simplicity, we assume all functions are computable by constant-depth circuits
        return True
    
    def sipser_function(n):
        return [1 if i % 2 == 0 else -1 for i in range(1 << n)]
    
    def random_function(n):
        return [random.choice([-1, 1]) for _ in range(1 << n)]
    
    def metric_value(fourier_coeffs, n):
        max_coeff = max(abs(coeff) for coeff in fourier_coeffs)
        threshold = Fraction(1, (n ** 0.5))
        return max_coeff >= threshold
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    support_count = 0
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different functions
            f = sipser_function(n) if random.random() < 0.5 else random_function(n)
            fourier_coeffs = fourier_transform(f, n)
            if metric_value(fourier_coeffs, n):
                instances_tested += 1
                if not is_acc0_circuit(f, n, 2 ** (n // 2)):
                    support_count += 1
                else:
                    counterexample = "Sipser function or random function computable by ACC0 circuit"
    
    conjecture_holds = support_count / instances_tested >= 0.8 if instances_tested > 0 else False
    
    return {
        "metric_name": "Fourier Coefficient Concentration",
        "metric_value": support_count / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 103))  # First 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")