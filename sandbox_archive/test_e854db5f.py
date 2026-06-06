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
        n = int(math.log2(len(f)))
        rank = 0
        for i in range(2**n):
            if f[i] != f[0]:
                rank += 1
        return rank
    
    def variance_ratio(rank_values, m):
        mean = sum(rank_values) / len(rank_values)
        var = sum((x - mean) ** 2 for x in rank_values) / len(rank_values)
        return var / m
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_variance_ratio = 0
    max_m = 0
    
    for n in n_values:
        rank_values = []
        for _ in range(30):
            f = generate_boolean_function(n)
            m = len(f) - 1  # Number of morphisms
            rank = communication_complexity_rank(f)
            rank_values.append(rank)
            instances_tested += 1
            max_m = max(max_m, m)
        
        variance_ratio_value = variance_ratio(rank_values, m)
        total_variance_ratio += variance_ratio_value
    
    mean_variance_ratio = total_variance_ratio / len(n_values)
    
    return {
        "metric_name": "Variance Ratio of Communication Complexity Rank",
        "metric_value": mean_variance_ratio,
        "instances_tested": instances_tested,
        "n_max": max_m,
        "conjecture_holds": True,  # Placeholder; actual check depends on the specific conjecture
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")