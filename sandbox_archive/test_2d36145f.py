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
    
    def xor_and_tree_width(f):
        if len(f) == 1:
            return 0
        else:
            left = f[:len(f)//2]
            right = f[len(f)//2:]
            return max(xor_and_tree_width(left), xor_and_tree_width(right)) + 1
    
    def characteristic_polynomial(f):
        n = len(f)
        if n == 1:
            return [f[0]]
        else:
            left_poly = characteristic_polynomial(f[:n//2])
            right_poly = characteristic_polynomial(f[n//2:])
            result = [0] * (len(left_poly) + len(right_poly) - 1)
            for i in range(len(left_poly)):
                for j in range(len(right_poly)):
                    result[i+j] += left_poly[i] * right_poly[j]
            return result
    
    def brauer_group_degree(poly):
        n = len(poly)
        if n == 1:
            return 0
        else:
            degree = 0
            for i in range(1, n):
                if poly[i] != 0:
                    degree += 1
            return degree
    
    max_n = 40
    degrees = []
    widths = []
    
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.randint(5, max_n)
        f = [random.choice([0, 1]) for _ in range(n)]
        width = xor_and_tree_width(f)
        poly = characteristic_polynomial(f)
        degree = brauer_group_degree(poly)
        
        degrees.append(degree)
        widths.append(width)
    
    correlation_coefficient = sum((d - mean_d) * (w - mean_w) for d, w in zip(degrees, widths)) / (n_tested * std_d * std_w)
    p_value = 2 * (1 - abs(correlation_coefficient))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": n_tested,
        "conjecture_holds": correlation_coefficient >= 0.7 and p_value <= 0.05,
        "counterexample": "" if correlation_coefficient >= 0.7 and p_value <= 0.05 else f"correlation={correlation_coefficient}, p-value={p_value}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))  # Default to first 30 primes
    
    results = []
    n_tested = 0
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
        n_tested += result["instances_tested"]
    
    mean_d = sum(r["metric_value"] for r in results) / len(results)
    std_d = (sum((r["metric_value"] - mean_d)**2 for r in results) / len(results))**0.5
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_d} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")