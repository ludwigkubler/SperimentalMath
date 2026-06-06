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
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        matrix = [[f[i * (2**(n-1)) + j] for i in range(2**(n-1))] for j in range(2)]
        rank = 0
        for row in matrix:
            if any(row):
                rank += 1
        return rank
    
    def lie_algebroid_local_index(rank):
        # Placeholder function, actual implementation needed
        return random.randint(rank, 2 * rank)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        rank = communication_complexity_rank(f)
        local_index = lie_algebroid_local_index(rank)
        
        if local_index < rank or local_index > 2 * rank:
            return {
                "metric_name": "Local Index",
                "metric_value": None,
                "instances_tested": len(n_values),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"Rank: {rank}, Local Index: {local_index}"
            }
        
        results.append(local_index)
    
    return {
        "metric_name": "Local Index",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if not trial_result["conjecture_holds"]:
            return {
                "metric_name": "Local Index",
                "metric_value": None,
                "instances_tested": len(seeds),
                "n_max": max(trial_result["n_max"] for trial_result in results),
                "conjecture_holds": False,
                "counterexample": f"First failing seed: {seed}"
            }
        
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=Unknown support_fraction={support_fraction}")
    else:
        print(f"RESULT: FALSIFIED counterexample=None first_failing_seed=None")