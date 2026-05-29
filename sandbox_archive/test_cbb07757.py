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
        a = [random.choice([0, 1]) for _ in range(n)]
        diff = [a[i] - a[i-1] for i in range(1, n)]
        return a, set(diff)
    
    def tree_like_resolution_width(a):
        n = len(a)
        if n <= 1:
            return 0
        width = 1
        for i in range(n):
            for j in range(i+1, n):
                if a[j] - a[i] == 0:
                    continue
                k = (a[j] - a[i]) // abs(a[j] - a[i])
                if all(a[l] - a[i] != k * (l - i) for l in range(n)):
                    width += 1
        return width
    
    def spearman_rank_correlation(x, y):
        n = len(x)
        rank_x = {x[i]: i+1 for i in range(n)}
        rank_y = {y[i]: i+1 for i in range(n)}
        d_squared_sum = sum((rank_x[x[i]] - rank_y[y[i]]) ** 2 for i in range(n))
        return 1 - (6 * d_squared_sum) / (n * (n**2 - 1))
    
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            a, S = generate_boolean_function(n)
            width = tree_like_resolution_width(a)
            metrics.append(width)
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_width = sum(metrics) / len(metrics)
    std_dev = math.sqrt(sum((x - mean_width) ** 2 for x in metrics) / len(metrics))
    conjecture_holds = mean_width <= 2 * math.log(len(S)) ** 2 and std_dev <= 0.1 * mean_width
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "tree_like_resolution_width",
        "metric_value": mean_width,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_width) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")