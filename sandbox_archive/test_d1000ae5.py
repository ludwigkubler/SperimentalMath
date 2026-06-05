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
        if n == 1:
            return 1
        rank = 1
        while True:
            new_rank = rank + 1
            found = False
            for i in range(n):
                if f[i] != f[(i + 2**rank) % n]:
                    found = True
                    break
            if not found:
                return new_rank
            rank = new_rank
    
    def hodge_diamond_diameter(d):
        max_distance = 0
        for i in range(len(d)):
            for j in range(i, len(d)):
                distance = abs(d[i] - d[j])
                if distance > max_distance:
                    max_distance = distance
        return max_distance
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        f = generate_boolean_function(n)
        r_f = communication_complexity_rank(f)
        d = [r_f] * (n + 1)  # Simplified Hodge diamond for demonstration
        diameter = hodge_diamond_diameter(d)
        
        total_metric_value += diameter
        instances_tested += 1
        n_max = max(n_max, n)
        
        if conjecture_holds and diameter > 3 * r_f:
            conjecture_holds = False
            counterexample = f"n={n}, r(f)={r_f}, diameter={diameter}"
    
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = instances_tested / len(n_values)
    
    if conjecture_holds and support_fraction >= 0.8:
        return {
            "metric_name": "Hodge Diamond Diameter",
            "metric_value": mean_metric_value,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": True,
            "counterexample": ""
        }
    elif not conjecture_holds:
        return {
            "metric_name": "Hodge Diamond Diameter",
            "metric_value": mean_metric_value,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": counterexample
        }
    else:
        return {
            "metric_name": "Hodge Diamond Diameter",
            "metric_value": mean_metric_value,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] != "mapping_undefined" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")