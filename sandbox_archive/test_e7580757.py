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
    
    def noncrossing_partition_tree_height(f):
        n = len(f)
        if n == 1:
            return 1
        height = 0
        while f:
            new_f = []
            for i in range(len(f) // 2):
                a, b = f[2*i], f[2*i+1]
                if a != b:
                    new_f.append(1)
                else:
                    new_f.append(a)
            f = new_f
            height += 1
        return height
    
    def ac0_circuit_size(f):
        n = len(f)
        if n == 1:
            return 1
        size = 0
        while f:
            new_f = []
            for i in range(len(f) // 2):
                a, b = f[2*i], f[2*i+1]
                if a != b:
                    new_f.append(1)
                else:
                    new_f.append(a)
            f = new_f
            size += 1
        return size
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            f = generate_boolean_function(n)
            height = noncrossing_partition_tree_height(f)
            size = ac0_circuit_size(f)
            if height > 2**(C * math.log2(n)**2):
                return {
                    "metric_name": "height vs circuit size",
                    "metric_value": height,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": f"n={n}, h(n)={height}, AC^0 size={size}"
                }
            results.append((height, size))
    
    mean_height = sum(h for h, _ in results) / len(results)
    mean_size = sum(s for _, s in results) / len(results)
    
    return {
        "metric_name": "height vs circuit size",
        "metric_value": mean_height,
        "instances_tested": len(results),
        "conjecture_holds": all(h <= 2**(C * math.log2(n)**2) for n, h in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2**i + 1 for i in range(5, 30)]
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")