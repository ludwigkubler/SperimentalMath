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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def geometric_entropy(f):
        n = len(f)
        counts = [f.count(i) for i in range(2)]
        probabilities = [c / n for c in counts]
        entropy = -sum(p * math.log2(p) if p > 0 else 0 for p in probabilities)
        return entropy
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        rank = 1
        for i in range(1, n + 1):
            if all(f[j] == f[j ^ (1 << i)] for j in range(2**n)):
                rank += 1
            else:
                break
        return rank ** 2
    
    def correlation_coefficient(data_x, data_y):
        mean_x = sum(data_x) / len(data_x)
        mean_y = sum(data_y) / len(data_y)
        cov_xy = sum((x - mean_x) * (y - mean_y) for x, y in zip(data_x, data_y)) / len(data_x)
        std_x = math.sqrt(sum((x - mean_x) ** 2 for x in data_x) / len(data_x))
        std_y = math.sqrt(sum((y - mean_y) ** 2 for y in data_y) / len(data_y))
        return cov_xy / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    mge_values = []
    rcv_values = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        mge = geometric_entropy(f)
        rcv = communication_complexity_rank_variance(f)
        mge_values.append(mge)
        rcv_values.append(rcv)
    
    correlation = correlation_coefficient(mge_values, rcv_values)
    mean_mge = sum(mge_values) / len(mge_values)
    std_mge = math.sqrt(sum((x - mean_mge) ** 2 for x in mge_values) / len(mge_values))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) >= 0.8 and std_mge <= 3,
        "counterexample": "" if abs(correlation) >= 0.8 and std_mge <= 3 else "correlation_threshold_not_met"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    std_corr = math.sqrt(sum((r["metric_value"] - mean_corr) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_threshold_not_met' first_failing_seed={first_failing_seed}")