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
    
    def p_adic_order(x, p):
        if x == 0:
            return float('inf')
        order = 0
        while x % p == 0:
            x //= p
            order += 1
        return order
    
    def xor_function(bits):
        result = bits[0]
        for bit in bits[1:]:
            result ^= bit
        return result
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        conjecture_holds = True
        counterexample = ""
        
        for _ in range(30):
            bits = [random.randint(0, 1) for _ in range(n)]
            f = xor_function(bits)
            
            min_p_order = float('inf')
            max_p_order = 0
            
            for p in range(2, n + 1):
                order = p_adic_order(f(p), p)
                if order < min_p_order:
                    min_p_order = order
                if order > max_p_order:
                    max_p_order = order
            
            instances_tested += 1
            
            # Check the first part of the conjecture: p-adic order at most Θ(n^(1/2))
            if min_p_order > n ** 0.5 * (1 + random.random() / 10):
                conjecture_holds = False
                counterexample = f"n={n}, min_p_order={min_p_order}"
            
            # Check the second part of the conjecture: p-adic order at least cn^(1/4)
            c = 0.5 * random.random()
            if max_p_order < c * n ** 0.25:
                conjecture_holds = False
                counterexample = f"n={n}, max_p_order={max_p_order}"
        
        results.append({
            "metric_name": "p-adic Order",
            "metric_value": (min_p_order + max_p_order) / 2,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    
    mean_metric = sum(result["metric_value"] for result in results) / len(results)
    std_metric = math.sqrt(sum((result["metric_value"] - mean_metric) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_metric": mean_metric,
        "std_metric": std_metric,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric = sum(result["mean_metric"] for result in results) / len(results)
    std_metric = math.sqrt(sum((result["mean_metric"] - mean_metric) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["support_fraction"] >= 0.8) / len(results)
    
    if support_fraction == 1:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction_too_low")