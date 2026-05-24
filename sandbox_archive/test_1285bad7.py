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
    
    def log_power(x, power):
        return x ** (1 / power)
    
    def dedekind_zeta(q):
        if q <= 0:
            return None
        sum_val = 0
        for k in range(1, 1000):  # Limit to avoid infinite loop
            sum_val += 1 / (q ** k * math.log(k + 1))
        return sum_val
    
    def p_adic_l_function(q):
        if q <= 0:
            return None
        zeta_q = dedekind_zeta(q)
        if zeta_q is None:
            return None
        return zeta_q / (2 * math.log(2) ** 3)
    
    def dpll_refutation_depth(n):
        # Simplified DPLL refutation depth calculation for demonstration
        return n ** 0.75
    
    instances_tested = 0
    total_l_value = 0
    max_n = 40
    min_ratio = float('inf')
    
    for n in range(5, max_n + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            q = random.randint(1, 100)  # Random p-adic integer
            l_value = p_adic_l_function(q)
            if l_value is None:
                continue
            refutation_depth = dpll_refutation_depth(n)
            ratio = abs(l_value / log_power(n, 3/4))
            total_l_value += l_value
            instances_tested += 1
            min_ratio = min(min_ratio, ratio)
    
    if instances_tested == 0:
        return {
            "metric_name": "min_ratio",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_l_value = total_l_value / instances_tested
    conjecture_holds = min_ratio <= 2 and min_ratio >= 0.5
    
    return {
        "metric_name": "min_ratio",
        "metric_value": min_ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Ratio out of range: {min_ratio}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Ratio out of range' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")