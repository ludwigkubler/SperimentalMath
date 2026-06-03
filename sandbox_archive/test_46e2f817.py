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
    
    def compute_grothendieck_group_order(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            return None
        G_f = set()
        for i in range(n):
            for j in range(i+1, n):
                x = sum(1 << k for k in range(n) if f[k] == (i < j))
                y = sum(1 << k for k in range(n) if f[k] == (j < i))
                G_f.add((x, y))
        return len(G_f)
    
    def circuit_monotone_width(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            return None
        width = 0
        for i in range(n):
            count = sum(1 for j in range(i+1, n) if f[j] < f[i])
            width = max(width, count)
        return width
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        g_order = compute_grothendieck_group_order(f)
        w_f = circuit_monotone_width(f)
        if g_order is None or w_f is None:
            continue
        results.append((g_order, w_f))
    
    if not results:
        return {
            "metric_name": "log(G_f)",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    log_g_orders = [math.log(g_order) for g_order, _ in results]
    w_fs = [w_f for _, w_f in results]
    correlation_coefficient = sum((log_g_orders[i] - mean(log_g_orders)) * (w_fs[i] - mean(w_fs)) for i in range(len(results))) / math.sqrt(sum((log_g_orders[i] - mean(log_g_orders))**2 for i in range(len(results)))) / math.sqrt(sum((w_fs[i] - mean(w_fs))**2 for i in range(len(results))))
    
    return {
        "metric_name": "log(G_f)",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": abs(correlation_coefficient) >= 1.96,
        "counterexample": "" if abs(correlation_coefficient) >= 1.96 else f"correlation_coefficient={correlation_coefficient}"
    }

def mean(lst):
    return sum(lst) / len(lst)

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r["metric_value"]) >= 1.96) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<1.96\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")