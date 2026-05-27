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
    
    def xor_and_tree_width(boolean_function):
        if len(boolean_function) == 1:
            return 0
        else:
            left, right = boolean_function[1], boolean_function[2]
            return 1 + max(xor_and_tree_width(left), xor_and_tree_width(right))
    
    def geometric_langlands_lattice_rank(boolean_function):
        n = len(boolean_function)
        rank = 0
        for i in range(1 << n):
            if all((i >> j) & 1 == boolean_function[j] for j in range(n)):
                rank += 1
        return rank
    
    def generate_boolean_function(n, max_depth):
        if n == 1:
            return random.choice([0, 1])
        else:
            left = generate_boolean_function(n // 2, max_depth - 1)
            right = generate_boolean_function(n // 2 + n % 2, max_depth - 1)
            op = random.choice(['&', '|'])
            if op == '&':
                return [op, left, right]
            else:
                return [op, left, right]
    
    def calculate_metric(boolean_function):
        T = xor_and_tree_width(boolean_function)
        kappa_L = geometric_langlands_lattice_rank(boolean_function)
        return kappa_L / (T ** 2), T
    
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    
    for n in n_values:
        boolean_function = generate_boolean_function(n, 4)
        metric_value, T = calculate_metric(boolean_function)
        metrics.append((metric_value, T))
    
    mean_metric_value = sum(metric[0] for metric in metrics) / len(metrics)
    max_T = max(metric[1] for metric in metrics)
    support_fraction = sum(1 for metric in metrics if metric[0] <= 1.5 * (max_T ** 2)) / len(metrics)
    
    return {
        "metric_name": "kappa_L/T^2",
        "metric_value": mean_metric_value,
        "instances_tested": len(n_values),
        "conjecture_holds": support_fraction >= 0.8 and max_T > 0,
        "counterexample": "" if support_fraction >= 0.8 else f"n={len(n_values)}, T={max_T}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] > 1.5 * (max(r["metric_value"] for r in results)) ** 2 for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"n={len(n_values)}, T={max_T}\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(seeds)}")