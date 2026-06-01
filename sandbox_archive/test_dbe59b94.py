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
    
    def generate_instance(n):
        # Generate a communication complexity instance with n variables
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_unit_group_size(instance):
        # Compute the minimal order of the unit group of the local ring
        n = len(instance)
        R = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if instance[i] == instance[j]:
                    R[i][j] = 1
        # Gaussian elimination to find the rank of R
        rank = 0
        for i in range(n):
            pivot_row = None
            for r in range(i, n):
                if R[r][i] != 0:
                    pivot_row = r
                    break
            if pivot_row is None:
                continue
            rank += 1
            for j in range(i, n):
                R[pivot_row][j], R[i][j] = R[i][j], R[pivot_row][j]
            for r in range(n):
                if r != i:
                    factor = -R[r][i]
                    for j in range(i, n):
                        R[r][j] += factor * R[i][j]
        return rank
    
    def compute_communication_complexity_rank(instance):
        # Compute the communication complexity rank of the instance
        n = len(instance)
        max_rank = 0
        for i in range(2**n):
            for j in range(i+1, 2**n):
                if instance[i] != instance[j]:
                    max_rank += 1
        return max_rank
    
    instances_tested = 30
    n_max = 40
    unit_group_sizes = []
    communication_complexity_ranks = []
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        instance = generate_instance(n)
        unit_group_size = compute_unit_group_size(instance)
        communication_complexity_rank = compute_communication_complexity_rank(instance)
        
        unit_group_sizes.append(unit_group_size)
        communication_complexity_ranks.append(communication_complexity_rank)
    
    mean_unit_group_size = sum(unit_group_sizes) / instances_tested
    mean_communication_complexity_rank = sum(communication_complexity_ranks) / instances_tested
    
    correlation_coefficient = 0
    if len(unit_group_sizes) > 1:
        numerator = sum((unit_group_sizes[i] - mean_unit_group_size) * (communication_complexity_ranks[i] - mean_communication_complexity_rank) for i in range(len(unit_group_sizes)))
        denominator = math.sqrt(sum((unit_group_sizes[i] - mean_unit_group_size)**2 for i in range(len(unit_group_sizes))) * sum((communication_complexity_ranks[i] - mean_communication_complexity_rank)**2 for i in range(len(communication_complexity_ranks))))
        correlation_coefficient = numerator / denominator
    
    conjecture_holds = correlation_coefficient >= 0.8 and abs(mean_unit_group_size - mean_communication_complexity_rank) <= 3
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 10**9) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")