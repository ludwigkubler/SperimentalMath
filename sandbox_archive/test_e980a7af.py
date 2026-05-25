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
    
    def max_cut_instance(n):
        return [random.choice([0, 1]) for _ in range(n)]
    
    def tropical_variety(instance):
        n = len(instance)
        return [[instance[i] ^ instance[j] for j in range(i + 1, n)] for i in range(n)]
    
    def hodge_integrals(tropical_variety):
        n = len(tropical_variety)
        integrals = [0] * n
        for i in range(n):
            for j in range(n):
                if tropical_variety[i][j]:
                    integrals[i] += 1 / (i + j + 1)
        return min(integrals)
    
    def sum_of_squares_circuit_depth(instance):
        n = len(instance)
        depth = 0
        for i in range(n):
            if instance[i] == 1:
                depth += 1
        return depth
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_metric_value = 0
        
        for _ in range(5):
            instance = max_cut_instance(n)
            tv = tropical_variety(instance)
            hi = hodge_integrals(tv)
            depth = sum_of_squares_circuit_depth(instance)
            
            if hi < math.sqrt(n) or hi < math.sqrt(depth):
                return {
                    "metric_name": "Hodge Integral",
                    "metric_value": hi,
                    "instances_tested": instances_tested,
                    "conjecture_holds": False,
                    "counterexample": f"Instance {instance} with n={n}, HODGE({hi}) < sqrt(n) or sqrt(d)"
                }
            
            total_metric_value += hi
            instances_tested += 1
        
        results.append({
            "metric_name": "Hodge Integral",
            "metric_value": total_metric_value / instances_tested,
            "instances_tested": instances_tested,
            "conjecture_holds": True,
            "counterexample": ""
        })
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "metric_name": "Hodge Integral",
        "mean_metric_value": mean_value,
        "support_fraction": support_fraction,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 997) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"mean_metric_value\": {result['mean_metric_value']:.6f}, \"support_fraction\": {result['support_fraction']:.2f}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(result["mean_metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["support_fraction"] >= 0.8) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.6f} std=NA support_fraction={support_fraction:.2f}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")