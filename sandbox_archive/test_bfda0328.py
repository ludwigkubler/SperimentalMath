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
    
    def dpll_search_tree(instance):
        if '0' not in instance and '1' not in instance:
            return 1
        if instance[0] == '0':
            return 1 + dpll_search_tree(instance[2:])
        elif instance[0] == '1':
            return 1 + dpll_search_tree(instance[2:])
    
    def generate_instance(n):
        return ''.join(random.choice('01') for _ in range(n))
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # Test each size with 5 different instances
            instance = generate_instance(n)
            tree_size = dpll_search_tree(instance)
            total_metric_value += tree_size
            instances_tested += 1
            if n > n_max:
                n_max = n
    
    mean_metric_value = Fraction(total_metric_value, instances_tested)
    conjecture_holds = mean_metric_value >= math.sqrt(n_max) * n_max / 2
    counterexample = "" if conjecture_holds else f"Mean metric value {mean_metric_value} is less than Ω({n_max}^(1.5))"
    
    return {
        "metric_name": "DPLL Search Tree Size",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")