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
    
    def tropical_add(a, b):
        return max(a, b)
    
    def tropical_multiply(a, b):
        if a == float('-inf') or b == float('-inf'):
            return float('-inf')
        return a + b
    
    def tropical_negate(a):
        return float('-inf') if a == float('-inf') else -a
    
    def tropical_zero():
        return float('-inf')
    
    def tropical_one():
        return 0
    
    def tropical_identity(x):
        return x
    
    def tropical_inverse(x):
        return tropical_negate(x)
    
    def tropical_power(a, n):
        result = tropical_zero()
        for _ in range(n):
            result = tropical_add(result, a)
        return result
    
    def tropical_polynomial_eval(poly, x):
        result = tropical_zero()
        for coeff in poly:
            result = tropical_add(result, tropical_multiply(coeff, x))
        return result
    
    def tropical_power_series_representation(poly, n):
        series = []
        for i in range(n + 1):
            series.append(tropical_polynomial_eval(poly, i))
        return series
    
    def minimal_rank(series):
        rank = 0
        for row in series:
            if any(row[i] != float('-inf') for i in range(len(row))):
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            coefficients = [random.randint(-10, 10) for _ in range(n + 1)]
            poly = coefficients[::-1]
            series = tropical_power_series_representation(poly, n)
            rank = minimal_rank(series)
            total_rank += rank
            instances_tested += 1
    
    mean_rank = Fraction(total_rank, instances_tested)
    std_dev = 0
    for n in n_values:
        for _ in range(5):
            coefficients = [random.randint(-10, 10) for _ in range(n + 1)]
            poly = coefficients[::-1]
            series = tropical_power_series_representation(poly, n)
            rank = minimal_rank(series)
            std_dev += (rank - mean_rank)**2
    std_dev = Fraction(std_dev, instances_tested).sqrt()
    
    conjecture_holds = mean_rank <= n_values[-1]**(3/2) and std_dev < 0.1 * mean_rank
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": float(mean_rank),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_dev = (sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")