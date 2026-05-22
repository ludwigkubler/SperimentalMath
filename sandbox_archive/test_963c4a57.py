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

def generate_disjointness_instance(n):
    return [random.sample(range(1, 2*n), n) for _ in range(2)]

def compute_matroid_rank(instance):
    n = len(instance[0])
    matroid = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if instance[0][i] < instance[1][j]:
                matroid[i].append(j)
    
    rank = 0
    while True:
        independent_set = []
        for i in range(n):
            if all(matroid[j] == [] for j in independent_set) and any(matroid[i]):
                independent_set.append(i)
        
        if not independent_set:
            break
        
        rank += 1
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instance = generate_disjointness_instance(n)
        rank = compute_matroid_rank(instance)
        
        communication_complexity = len(instance[0]) + len(instance[1])
        
        results.append({
            "n": n,
            "rank": rank,
            "communication_complexity": communication_complexity
        })
    
    total_instances_tested = sum(result["instances_tested"] for result in results)
    mean_rank = sum(result["rank"] * result["instances_tested"] for result in results) / total_instances_tested
    std_rank = math.sqrt(sum((result["rank"] - mean_rank)**2 * result["instances_tested"] for result in results) / total_instances_tested)
    
    conjecture_holds = all(result["rank"] >= n for result in results)
    counterexample = "" if conjecture_holds else "n={n}, rank={rank}"
    
    return {
        "metric_name": "Rank of Noncrossing Partitions",
        "metric_value": mean_rank,
        "instances_tested": total_instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] * result["instances_tested"] for result in results) / sum(result["instances_tested"] for result in results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank)**2 * result["instances_tested"] for result in results) / sum(result["instances_tested"] for result in results))
    
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = f"n={result['n']}, rank={result['rank']}"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")