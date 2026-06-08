# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = len(f)
        rank = 0
        for i in range(n):
            if f[i] != f[0]:
                rank += 1
        return rank
    
    def monodromy_group_order(f):
        # Placeholder function to simulate the computation of the monodromy group order
        # This is a dummy implementation and should be replaced with an actual algorithm
        n = len(f)
        return n + 1
    
    def variance(lst):
        mean = sum(lst) / len(lst)
        return sum((x - mean)**2 for x in lst) / len(lst)
    
    instances_tested = 0
    metric_values = []
    n_max = 5
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Test each size 5 times
            f = generate_boolean_function(n)
            comm_rank_var = variance([communication_complexity_rank(f) for _ in range(10)])
            g_f = monodromy_group_order(f)
            instances_tested += 1
            n_max = max(n_max, n)
            metric_values.append(g_f)
    
    if not instances_tested:
        return {
            "metric_name": "monodromy_group_order",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_metric = sum(metric_values) / instances_tested
    support_fraction = len([x for x in metric_values if abs(x - mean_metric) <= 3]) / instances_tested
    
    return {
        "metric_name": "monodromy_group_order",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": support_fraction >= 0.8 and mean_metric <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    metric_mean = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / sum(1 for r in results if r["metric_value"] is not None)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={metric_mean} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] != "" for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")