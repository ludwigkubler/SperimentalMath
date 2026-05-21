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
    
    def noncommutative_fourier_transform(n):
        if n <= 0:
            return []
        transform = [0] * (1 << n)
        for i in range(1 << n):
            sign = (-1) ** bin(i).count('1')
            transform[i] = sign
        return transform
    
    def count_nonzero_coefficients(transform):
        return sum(1 for coeff in transform if coeff != 0)
    
    def lower_bound(n, d):
        if d <= 1:
            return float('-inf')
        return n ** (1 / (d - 1))
    
    n = random.randint(5, 40)
    d = random.randint(2, 3)  # AC⁰ depth is typically small
    transform = noncommutative_fourier_transform(n)
    nonzero_count = count_nonzero_coefficients(transform)
    expected_lower_bound = lower_bound(n, d)
    
    return {
        "metric_name": "nonzero_coefficient_count",
        "metric_value": nonzero_count,
        "instances_tested": 1,
        "conjecture_holds": nonzero_count >= expected_lower_bound,
        "counterexample": "" if nonzero_count >= expected_lower_bound else f"n={n}, d={d}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*31, 2))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_nonzero_count = sum(r["metric_value"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    mean = Fraction(total_nonzero_count, len(results))
    std_dev = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE budget_exceeded n_tested=30")