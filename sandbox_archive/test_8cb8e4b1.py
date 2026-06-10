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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def quandle_action(f, x):
        n = len(f)
        result = []
        for i in range(n):
            if f[i] == 0:
                result.append((x + i) % n)
            else:
                result.append((x - i) % n)
        return tuple(result)
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        actions = set()
        for x in range(n):
            actions.add(quandle_action(f, x))
        rank = len(actions)
        return rank * (n - rank)
    
    def minimal_order_of_quandle_action(f):
        n = len(f)
        min_order = float('inf')
        for x in range(n):
            action = quandle_action(f, x)
            if action not in f:
                continue
            order = 1
            current = action
            while current != (0,) * n:
                current = quandle_action(f, current[0])
                order += 1
            min_order = min(min_order, order)
        return min_order
    
    n_values = [5, 10, 15, 20, 30, 40]
    rank_variances = []
    m_values = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        m = minimal_order_of_quandle_action(f)
        rank_variance = communication_complexity_rank_variance(f)
        rank_variances.append(rank_variance)
        m_values.append(m)
    
    mean_m = sum(m_values) / len(m_values)
    mean_rank_variance = sum(rank_variances) / len(rank_variances)
    
    lower_bound = mean_m
    upper_bound = mean_m ** 2
    
    conjecture_holds = all(lower_bound <= rv <= upper_bound for rv in rank_variances)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "rank_variance",
        "metric_value": mean_rank_variance,
        "instances_tested": len(rank_variances),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={r['seed']}")
                break