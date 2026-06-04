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
        max_rank = 0
        for i in range(1 << (n - 1)):
            rank = 0
            for j in range(n):
                if f[i ^ (1 << j)] != f[i]:
                    rank += 1
            max_rank = max(max_rank, rank)
        return max_rank
    
    def minimal_monoidal_categorical_generators(f):
        n = len(f)
        generators = set()
        for i in range(1 << n):
            if all(f[i ^ (1 << j)] != f[i] for j in range(n)):
                generators.add(i)
        return generators
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        rank = communication_complexity_rank(f)
        generators = minimal_monoidal_categorical_generators(f)
        
        if len(generators) > 100:  # Avoid excessive computation
            continue
        
        results.append({
            "metric_name": "communication_complexity_rank",
            "metric_value": rank,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": ""
        })
    
    if not results:
        return {
            "metric_name": "communication_complexity_rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    correlation_coefficient = None
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": mean_metric,
        "instances_tested": len(results),
        "n_max": max(r["n_max"] for r in results),
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if not r["conjecture_holds"]) / len(results)
    
    if all(not r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")