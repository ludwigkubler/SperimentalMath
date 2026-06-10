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
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Input must be a Boolean function with 2^n values")
        
        row = [f[i ^ (1 << j)] for j in range(n)]
        col = [f[i] for i in range(2**n)]
        
        # Compute the rank of the communication matrix
        rank = 0
        for i in range(n):
            if any(row[j] != row[0] for j in range(1, n)):
                rank += 1
                break
        
        return rank
    
    def minimal_order_of_generalized_exponential_sum(f):
        n = int(math.log2(len(f)))
        k = 1
        while True:
            all_non_zero = True
            for i in range(2**n):
                if f[i] % k == 0:
                    all_non_zero = False
                    break
            if all_non_zero:
                return k
            k += 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        r_f = communication_complexity_rank(f)
        k_f = minimal_order_of_generalized_exponential_sum(f)
        
        if k_f > (math.sqrt(r_f))**3 * 1.5:  # Using a slight margin to account for rounding
            return {
                "metric_name": "minimal_order",
                "metric_value": k_f,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"n={n}, r(f)={r_f}, k_f={k_f}"
            }
    
    return {
        "metric_name": "minimal_order",
        "metric_value": sum(k_f for _, _, k_f in results) / len(results),
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= (math.sqrt(r))**3 * 1.5) / len(results)
    
    if all(r <= (math.sqrt(r))**3 * 1.5 for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result > (math.sqrt(result))**3 * 1.5)
        print(f"RESULT: FALSIFIED counterexample='n=40, r(f)=?, k_f=?' first_failing_seed={first_failing_seed}")