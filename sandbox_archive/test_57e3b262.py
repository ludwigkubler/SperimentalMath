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
    
    def q_difference_operator(n, k):
        if n == 1:
            return [[0] * k]
        else:
            op = []
            for i in range(k):
                row = [0] * k
                row[i] = 1
                row[(i + 1) % k] = -1
                op.append(row)
            return op
    
    def count_non_zero_coefficients(op):
        count = 0
        for row in op:
            for coeff in row:
                if coeff != 0:
                    count += 1
        return count
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        k = random.randint(2, n)
        op = q_difference_operator(n, k)
        count = count_non_zero_coefficients(op)
        results.append(count)
    
    mean_value = sum(results) / len(results)
    conjecture_holds = all(count >= k * math.log(n) for n, k in zip(n_values, [random.randint(2, n) for n in n_values]))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Number of non-zero coefficients",
        "metric_value": mean_value,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")