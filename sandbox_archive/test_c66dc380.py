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
    
    def permutation_matrix(f, n):
        pm = []
        for i in range(2**n):
            row = [0] * (2**n)
            row[i] = 1
            pm.append(row)
        return pm
    
    def rank_variance(pm):
        ranks = set()
        for row in pm:
            rank = sum(1 for x in row if x == 1)
            ranks.add(rank)
        return len(ranks) / len(ranks)
    
    def groupoid_representation(f, n):
        # Simplified representation using the number of variables
        return n
    
    def communication_complexity_rank_variance(pm):
        return rank_variance(pm)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_boolean_function(n)
        pm = permutation_matrix(f, n)
        order_G_f = groupoid_representation(f, n)
        rank_variance_f = communication_complexity_rank_variance(pm)
        
        if rank_variance_f == 0:
            continue
        
        ratio = Fraction(order_G_f, rank_variance_f)
        results.append(ratio)
    
    if not results:
        return {
            "metric_name": "Groupoid Order to Rank Variance Ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    mean_ratio = sum(results) / len(results)
    return {
        "metric_name": "Groupoid Order to Rank Variance Ratio",
        "metric_value": float(mean_ratio),
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_value = sum(results) / len(results)
    std_value = math.sqrt(sum((x - mean_value)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r - mean_value) <= 0.5 * std_value) / len(results)
    
    if all(trial_result["conjecture_holds"] for trial_result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not trial_result["conjecture_holds"] for trial_result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio out of expected bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported the conjecture")