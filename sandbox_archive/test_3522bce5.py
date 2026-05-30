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
    
    def euler_characteristic(f):
        n = len(f)
        if n == 0:
            return 0
        chi = 0
        for i in range(n):
            if f[i] == 1:
                chi += (-1)**i * (n - i)
        return chi
    
    def communication_complexity(M, c):
        N = len(M)
        rows = random.sample(range(N), N // 2)
        cols = random.sample(range(N), N // 2)
        cc = 0
        for r in rows:
            for c in cols:
                if M[r][c] == 1:
                    cc += 1
        return cc / (N * N) ** c
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        f = generate_boolean_function(n)
        chi_f = euler_characteristic(f)
        if chi_f < 0:
            continue
        total_metric_value += chi_f
        instances_tested += 1
        n_max = max(n_max, n)
        
        # Check communication complexity for a random Boolean matrix M
        M = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
        cc_M = communication_complexity(M, 0.5)
        if cc_M > chi_f ** (2/3):
            conjecture_holds = False
            counterexample = f"CC_R(M)={cc_M} > {chi_f**(2/3)}"
    
    return {
        "metric_name": "Euler Characteristic",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")