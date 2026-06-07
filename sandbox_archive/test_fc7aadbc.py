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
    
    def communication_complexity_rank(f):
        n = len(f)
        rank = 0
        for i in range(n):
            for j in range(i+1, n):
                if f[i] != f[j]:
                    rank += 1
        return rank
    
    def quandle(f):
        n = len(f)
        Q = {}
        for i in range(2**n):
            Q[i] = set()
        for x in range(2**n):
            for y in range(2**n):
                if f[x ^ y] == 1:
                    Q[x].add(y)
        return Q
    
    def min_order(Q):
        orders = [len(Q[x]) for x in Q]
        return min(orders) if orders else 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        r_f = communication_complexity_rank(f)
        Q_f = quandle(f)
        min_order_Q_f = min_order(Q_f)
        
        results.append({
            "n": n,
            "r_f": r_f,
            "min_order_Q_f": min_order_Q_f
        })
    
    mean_r_f = sum(result["r_f"] for result in results) / len(results)
    mean_min_order_Q_f = sum(result["min_order_Q_f"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["min_order_Q_f"] - mean_min_order_Q_f)**2 for result in results) / len(results))
    
    conjecture_holds = all(abs(result["min_order_Q_f"] - result["r_f"]) <= 3 * std_dev for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_order_vs_r_f",
        "metric_value": mean_min_order_Q_f,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")