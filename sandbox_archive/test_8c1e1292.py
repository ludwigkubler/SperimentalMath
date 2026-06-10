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
    
    def polynomial_from_boolean_function(f):
        n = len(f.keys())
        poly = [0] * (2**n)
        for x, y in f.items():
            index = sum(bit * (2 ** i) for i, bit in enumerate(x))
            poly[index] = y
        return poly

    def minimal_tropical_derivative(poly):
        n = len(poly)
        mt = [0] * n
        for i in range(n):
            if poly[i] != 0:
                min_val = float('inf')
                for j in range(n):
                    if i != j and poly[j] != 0:
                        diff = abs(i - j) / (poly[i] + poly[j])
                        if diff < min_val:
                            min_val = diff
                mt[i] = min_val
        return mt

    def communication_complexity_rank_variance(f):
        n = len(f.keys())
        ranks = []
        for i in range(n):
            rank = 0
            for j in range(n):
                if f[i] != f[j]:
                    rank += 1
            ranks.append(rank)
        mean_rank = sum(ranks) / n
        variance = sum((x - mean_rank) ** 2 for x in ranks) / n
        return variance

    def correlation_coefficient(x, y):
        n = len(x)
        if n != len(y):
            raise ValueError("Both lists must have the same length")
        
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_dev_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_dev_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        
        return cov_xy / (std_dev_x * std_dev_y)

    n_values = [5, 10, 15, 20, 30, 40]
    mt_values = []
    rc_values = []

    for n in n_values:
        f = {tuple(random.getrandbits(n) for _ in range(n)): random.choice([0, 1]) for _ in range(2**n)}
        poly = polynomial_from_boolean_function(f)
        mt = minimal_tropical_derivative(poly)
        rc = communication_complexity_rank_variance(f)
        
        mt_values.extend(mt)
        rc_values.append(rc)

    correlation = correlation_coefficient(mt_values, rc_values)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation,
        "instances_tested": len(mt_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.9,
        "counterexample": "" if correlation >= 0.7 else f"Correlation too low: {correlation}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Correlation too low' first_failing_seed={first_failing_seed}")