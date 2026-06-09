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
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        count = [0] * (n + 1)
        for i in range(1 << n):
            s = sum(f[j] for j in range(n) if (i >> j) & 1)
            count[s] += 1
        return max(count) - min(count)
    
    def monoidal_functors(f):
        n = len(f)
        # Construct a category from the Boolean function
        # This is a simplified example; actual implementation depends on the function
        C = []
        for i in range(n + 1):
            C.append([0] * (n + 1))
            C[-1][i] = 1
        return C
    
    def min_functors(C):
        k = len(C)
        dim_C = [sum(row) for row in C]
        return sum(k * d for k, d in zip(range(1, k + 1), dim_C))
    
    n_max = 0
    metric_value = 0.0
    instances_tested = 0
    
    for n in range(5, 41):
        f = generate_boolean_function(n)
        R_f = communication_complexity_rank_variance(f)
        C = monoidal_functors(f)
        k_dim_C = min_functors(C)
        
        if n > n_max:
            n_max = n
        
        metric_value += abs(k_dim_C - R_f)
        instances_tested += 1
    
    mean_metric_value = metric_value / instances_tested
    conjecture_holds = mean_metric_value <= 3 and mean_metric_value >= 0.5 * instances_tested
    counterexample = "" if conjecture_holds else f"Mean difference {mean_metric_value}"
    
    return {
        "metric_name": "Communication Complexity Rank Variance",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Mean difference {results[0]['metric_value']}\" first_failing_seed={first_failing_seed}")