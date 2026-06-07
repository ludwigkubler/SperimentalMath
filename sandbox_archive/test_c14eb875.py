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
    
    def construct_algebraic_variety(f):
        n = len(f)
        x = [0] * (n + 1)
        for i in range(n):
            if f[i] == '1':
                x[i] = 1
        return x
    
    def communication_complexity_rank(f):
        n = len(f)
        rank = 0
        for i in range(1, n):
            rank += math.log2(i + 1)
        return rank
    
    def hodge_diamond_diameter(poly):
        n = len(poly) - 1
        if n < 3:
            return 0
        d = [poly[i] * poly[n-i] for i in range(1, n//2+1)]
        return max(d)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = ''.join(random.choices(['0', '1'], k=n))
        poly = construct_algebraic_variety(f)
        rank = communication_complexity_rank(f)
        diameter = hodge_diamond_diameter(poly)
        results.append((diameter, rank))
    
    correlation_coefficient = 0
    if len(results) > 1:
        x_mean = sum(d for d, r in results) / len(results)
        y_mean = sum(r for d, r in results) / len(results)
        numerator = sum((d - x_mean) * (r - y_mean) for d, r in results)
        denominator = math.sqrt(sum((d - x_mean)**2 for d, r in results)) * math.sqrt(sum((r - y_mean)**2 for d, r in results))
        correlation_coefficient = numerator / denominator if denominator != 0 else 0
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": "" if correlation_coefficient >= 0.8 else "correlation_coefficient < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] == "correlation_coefficient < 0.8" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"] and result["counterexample"] == "correlation_coefficient < 0.8")
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data_or_other_reasons")