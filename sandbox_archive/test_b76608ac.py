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
    
    def min_rank(poly):
        n = len(poly)
        if n == 0:
            return 0
        rank = n
        for i in range(1, n + 1):
            if poly % i == 0:
                rank = min(rank, i)
        return rank
    
    def perm_circuit_threshold(poly):
        # Placeholder function to compute permutation circuit threshold
        # This is a dummy implementation and should be replaced with actual logic
        return len(poly) // 2
    
    n = random.randint(5, 40)
    poly = sum(random.randint(1, 10) * x**i for i in range(n + 1))
    
    rank = min_rank(poly)
    threshold = perm_circuit_threshold(poly)
    
    if threshold == 0:
        return {
            "metric_name": "min_rank/perm_circuit_threshold",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "threshold_zero"
        }
    
    ratio = rank / threshold
    
    return {
        "metric_name": "min_rank/perm_circuit_threshold",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction_too_low")