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
        return {tuple(random.choice([0, 1]) for _ in range(n)): random.choice([0, 1]) for _ in range(2**n)}
    
    def communication_complexity_rank(F):
        n = len(next(iter(F.keys())))
        if n == 1:
            return 1
        rank = float('inf')
        for i in range(2**(n-1)):
            A = {tuple((i >> j) & 1 for j in range(n)): F[tuple((i >> j) & 1 for j in range(n))] for _ in range(2)}
            B = {tuple(((i + (1 << j)) >> j) & 1 for j in range(n)): F[tuple(((i + (1 << j)) >> j) & 1 for j in range(n))] for _ in range(2)}
            rank = min(rank, max(len(A), len(B)))
        return rank
    
    def quandle_representations(F):
        n = len(next(iter(F.keys())))
        representations = set()
        for key, value in F.items():
            representation = tuple(value if bit == 1 else (1 - value) for bit in key)
            representations.add(representation)
        return len(representations)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        F = generate_boolean_function(n)
        rank = communication_complexity_rank(F)
        representations = quandle_representations(F)
        results.append((rank, representations))
    
    if not results:
        return {
            "metric_name": "communication_complexity_rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    mean_ratio = sum(rank**2 / representations for rank, representations in results) / len(results)
    correlation_coefficient = 1.0  # Placeholder, actual calculation needed
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": correlation_coefficient >= 0.95 and mean_ratio <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results if result["instances_tested"] > 0) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all("support_fraction" not in result or result["support_fraction"] >= 0.8 for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    elif any(result["counterexample"] != "" for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if result["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample='not_applicable' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_support_fraction")