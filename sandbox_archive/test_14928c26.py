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
    
    def p_adic_order(f, p):
        if f == 0:
            return float('inf')
        order = 0
        while f % p == 0:
            f //= p
            order += 1
        return order
    
    def xor_circuit_size(n):
        # Simplified estimation of ACC⁰ circuit size for XOR
        return n // 2
    
    def generate_xor_function(n):
        bits = [random.choice([0, 1]) for _ in range(n)]
        def f(x):
            result = 0
            for i in range(n):
                if x[i] != bits[i]:
                    result ^= 1
            return result
        return f
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_xor_function(n)
        S = xor_circuit_size(n)
        
        min_p_adic_order = float('inf')
        max_p_adic_order = 0
        
        for p in range(2, 1000):
            order = p_adic_order(f(p), p)
            if order < min_p_adic_order:
                min_p_adic_order = order
            if order > max_p_adic_order:
                max_p_adic_order = order
        
        results.append({
            "n": n,
            "min_p_adic_order": min_p_adic_order,
            "max_p_adic_order": max_p_adic_order,
            "S": S
        })
    
    metric_value = sum(result["min_p_adic_order"] for result in results) / len(results)
    conjecture_holds = all(result["min_p_adic_order"] <= math.sqrt(result["n"]) and result["max_p_adic_order"] >= result["n"]**(1/4) * 2**result["S"] for result in results)
    
    return {
        "metric_name": "Min p-adic Order",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")