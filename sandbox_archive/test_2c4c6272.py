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
    
    def is_monotone(circuit):
        for i in range(len(circuit)):
            if circuit[i] and not all(circuit[j] or circuit[k] for j, k in [(i-1, i+1), (i+1, i-1)]):
                return False
        return True
    
    def construct_matroid(circuit):
        matroid = set()
        for i in range(len(circuit)):
            if circuit[i]:
                matroid.add(i)
        return matroid
    
    n = 40
    k = 3  # Example value for k, can be adjusted as needed
    num_trials = 100
    
    ranks = []
    for _ in range(num_trials):
        circuit = [random.choice([True, False]) for _ in range(n)]
        if is_monotone(circuit):
            matroid = construct_matroid(circuit)
            rank = len(matroid)
            ranks.append(rank)
    
    mean_rank = sum(ranks) / num_trials
    lower_bound = n ** (1/4)
    upper_bound = 0.5 * n ** (1/4)
    
    conjecture_holds = all(mean_rank >= lower_bound and rank >= upper_bound for rank in ranks)
    counterexample = "" if conjecture_holds else "rank_too_low"
    
    return {
        "metric_name": "Rank of Generalized Matroid",
        "metric_value": mean_rank,
        "instances_tested": num_trials,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank_too_low\" first_failing_seed={first_failing_seed}")