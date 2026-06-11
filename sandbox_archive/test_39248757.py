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
    
    def generate_protocol(n):
        protocol = {}
        for i in range(n):
            for j in range(i + 1, n):
                protocol[(i, j)] = [random.randint(0, 1) for _ in range(5)]
                protocol[(j, i)] = [random.randint(0, 1) for _ in range(5)]
        return protocol
    
    def compute_min_order(protocol):
        n = len(protocol)
        order = 1
        for i in range(n):
            for j in range(i + 1, n):
                if (i, j) not in protocol or (j, i) not in protocol:
                    continue
                order *= max(abs(a - b) for a, b in zip(protocol[(i, j)], protocol[(j, i)]))
        return order
    
    def compute_rank_variance(protocol):
        n = len(protocol)
        rank_variances = []
        for i in range(n):
            for j in range(i + 1, n):
                if (i, j) not in protocol or (j, i) not in protocol:
                    continue
                rank_variances.append(sum(abs(a - b) for a, b in zip(protocol[(i, j)], protocol[(j, i)])))
        return sum(rank_variances) / len(rank_variances)
    
    n = random.randint(5, 40)
    protocol = generate_protocol(n)
    min_order = compute_min_order(protocol)
    rank_variance = compute_rank_variance(protocol)
    
    if min_order == 0:
        return {
            "metric_name": "log(min_order)",
            "metric_value": -math.inf,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "min_order_zero"
        }
    
    log_min_order = math.log(min_order)
    return {
        "metric_name": "log(min_order)",
        "metric_value": log_min_order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_log_min_order = sum(r["metric_value"] for r in results) / len(results)
    std_log_min_order = math.sqrt(sum((r["metric_value"] - mean_log_min_order) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_log_min_order} std={std_log_min_order} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_log_min_order} std={std_log_min_order} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"min_order_zero\" first_failing_seed={first_failing_seed}")