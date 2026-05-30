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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def euler_characteristic(f):
        n = len(f)
        count = 0
        for i in range(2**n):
            if f[i] == 1:
                count += (-1)**bin(i).count('1')
        return count
    
    def communication_complexity(M, c):
        N = len(M)
        total_bits = 0
        for _ in range(30):  # Sample 30 random subsets
            rows = random.sample(range(N), N // 2)
            cols = random.sample(range(N), N // 2)
            subset = [M[r][c] for r in rows for c in cols]
            total_bits += len(subset)
        return total_bits / (N * N)
    
    results = []
    n_max = 0
    
    for n in range(5, 41):
        f = generate_boolean_function(n)
        chi_f = euler_characteristic(f)
        if chi_f < 0:
            continue
        cc_f = communication_complexity([[f[i] * M[j][i] for i in range(n)] for j in range(n)], 3/2)
        results.append({"n": n, "chi_f": chi_f, "cc_f": cc_f})
        n_max = max(n_max, n)
    
    if len(results) < 30:
        return {
            "metric_name": "communication_complexity",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_cc = sum(result["cc_f"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["cc_f"] - mean_cc)**2 for result in results) / len(results))
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_cc,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": all(result["cc_f"] <= result["n"]**1.5 for result in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_dev_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all("counterexample" in result and result["counterexample"] != "" for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "counterexample" in result and result["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")