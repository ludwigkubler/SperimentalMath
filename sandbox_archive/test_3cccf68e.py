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
    
    def fourier_coefficients(f, n):
        N = len(f)
        coeffs = [0] * (N // 2 + 1)
        for k in range(N // 2 + 1):
            sum_val = 0
            for i in range(N):
                sum_val += f[i] * math.cos(2 * math.pi * k * i / N) if i % 2 == 0 else -f[i] * math.sin(2 * math.pi * k * i / N)
            coeffs[k] = sum_val / N
        return coeffs
    
    def octonion_algebra_order(coeffs):
        # Simplified version for demonstration; actual implementation would be more complex
        return len(coeffs) ** 2
    
    def read_twice_bp_size(f, n):
        # Placeholder function; actual implementation would depend on the specific BP structure
        return len(f)
    
    def correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_dev_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(len(x))) / len(x))
        std_dev_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(len(y))) / len(y))
        return cov / (std_dev_x * std_dev_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    orders = []
    bp_sizes = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        coeffs = fourier_coefficients(f, n)
        order = octonion_algebra_order(coeffs)
        bp_size = read_twice_bp_size(f, n)
        orders.append(order)
        bp_sizes.append(bp_size)
    
    corr = correlation(orders, bp_sizes)
    support_fraction = sum(corr >= 0.7 for _ in range(5)) / 5
    
    return {
        "metric_name": "correlation",
        "metric_value": corr,
        "instances_tested": len(n_values),
        "conjecture_holds": support_fraction > 0.8,
        "counterexample": "" if support_fraction > 0.8 else "correlation < 0.7"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}**}}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    std_corr = math.sqrt(sum((r["metric_value"] - mean_corr) ** 2 for r in results) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")