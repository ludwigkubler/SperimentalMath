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
    
    def geometric_entropy(f):
        n = int(math.log2(len(f)))
        counts = [f.count(i) for i in set(f)]
        probs = [c / len(f) for c in counts]
        entropy = -sum(p * math.log2(p) for p in probs if p > 0)
        return entropy
    
    def communication_complexity_rank_variance(f):
        n = int(math.log2(len(f)))
        # Simple random protocol
        protocol = [(i, f[i]) for i in range(n)]
        rank_variance = len(set(protocol)) / n
        return rank_variance
    
    def correlation_coefficient(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((x_i - mean_x) * (y_i - mean_y) for x_i, y_i in zip(x, y)) / len(x)
        std_x = math.sqrt(sum((x_i - mean_x)**2 for x_i in x) / len(x))
        std_y = math.sqrt(sum((y_i - mean_y)**2 for y_i in y) / len(y))
        return cov / (std_x * std_y)
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        f = generate_boolean_function(n)
        mge_f = geometric_entropy(f)
        rcv_f = communication_complexity_rank_variance(f)
        results.append((mge_f, rcv_f))
    
    if len(results) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mge = [r[0] for r in results]
    rcv = [r[1] for r in results]
    corr_coeff = correlation_coefficient(mge, rcv)
    mean_abs_diff = sum(abs(x - y) for x, y in zip(mge, rcv)) / len(mge)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": corr_coeff,
        "instances_tested": 30,
        "n_max": max(n_values),
        "conjecture_holds": corr_coeff >= 0.8 and mean_abs_diff <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_corr_coeff = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_corr_coeff = math.sqrt(sum((r["metric_value"] - mean_corr_coeff)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std={std_corr_coeff} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='not_supported' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")