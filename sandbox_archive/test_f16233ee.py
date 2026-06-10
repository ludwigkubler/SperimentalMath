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
    
    def generate_boolean_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def neg_unate_poly(circuit):
        n = len(circuit)
        for i in range(2**n):
            if circuit[i] == 1:
                continue
            found = True
            for j in range(n):
                if (i & (1 << j)) != 0 and circuit[i ^ (1 << j)] == 1:
                    found = False
                    break
            if found:
                return i
        return -1
    
    def tiling_rank(circuit):
        n = len(circuit)
        rank = 0
        for i in range(2**n):
            if circuit[i] == 1:
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        n_max = n
        total_metric_value = 0
        
        for _ in range(30):
            circuit = generate_boolean_circuit(n)
            neg_poly = neg_unate_poly(circuit)
            if neg_poly == -1:
                continue
            rank = tiling_rank(circuit)
            metric_value = math.exp(neg_poly) / rank
            instances_tested += 1
            total_metric_value += metric_value
        
        if instances_tested < 30:
            return {
                "metric_name": "Ratio",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": "insufficient_instances"
            }
        
        avg_metric = total_metric_value / instances_tested
        results.append(avg_metric)
    
    conjecture_holds = all(r >= 1 for r in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Ratio",
        "metric_value": sum(results) / len(results),
        "instances_tested": 30 * len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")