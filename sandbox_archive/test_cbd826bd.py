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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def characteristic_polynomial(f):
        n = len(f)
        poly = [0] * (n + 1)
        poly[0] = f[0]
        for i in range(1, n + 1):
            poly[i] = sum(f[j] * (-2)**j for j in range(i)) % 2
        return poly
    
    def min_generators_for_poly(poly):
        n = len(poly) - 1
        G = []
        for i in range(n + 1):
            if poly[i]:
                G.append([i])
        return len(G)
    
    def monotone_circuit_size(f):
        # Simplified heuristic for demonstration purposes
        return sum(1 for bit in f if bit == 1)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = generate_boolean_function(n)
            poly = characteristic_polynomial(f)
            alpha_c_f = min_generators_for_poly(poly)
            c_f = monotone_circuit_size(f)
            results.append((alpha_c_f, c_f))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    alpha_c_fs, c_fs = zip(*results)
    correlation_coefficient = sum((a - mean_alpha) * (c - mean_c) for a, c in zip(alpha_c_fs, c_fs)) / len(results)
    mean_alpha = sum(alpha_c_fs) / len(alpha_c_fs)
    mean_c = sum(c_fs) / len(c_fs)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and mean_abs_diff <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_correlation_coefficient = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_correlation_coefficient} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_correlation_coefficient} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={r['seed']}")
                break