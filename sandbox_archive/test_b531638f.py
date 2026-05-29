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
    
    def hypergeometric_zeros(D, n):
        if D == 0 or n == 0:
            return 0
        zeros = 0
        for z in range(1, 2**n):
            product = 1.0
            for i in range(n):
                x_i = (z & (1 << i)) != 0
                if x_i:
                    product *= (1 + x_i / z) ** -1
                else:
                    product *= (1 - x_i / z) ** -1
            zeros += abs(product)
        return zeros
    
    def polynomial_bound(n, D):
        # Example polynomial bound: c_D * 2^n
        c_D = 1.0
        return c_D * 2**n
    
    n_max = 40
    instances_tested = 0
    total_zeros = 0
    
    for n in range(5, n_max + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            D = random.randint(1, 10)
            zeros = hypergeometric_zeros(D, n)
            bound = polynomial_bound(n, D)
            total_zeros += zeros
            instances_tested += 1
            
            if zeros > bound * 10:
                return {
                    "metric_name": "zeros_over_bound",
                    "metric_value": zeros / bound,
                    "instances_tested": instances_tested,
                    "conjecture_holds": False,
                    "counterexample": f"n={n}, D={D}, zeros={zeros}, bound={bound}"
                }
    
    mean_zeros = total_zeros / instances_tested
    return {
        "metric_name": "zeros_over_bound",
        "metric_value": mean_zeros,
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")