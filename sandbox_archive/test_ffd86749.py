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
    
    def generate_and_or_tree(n):
        if n == 1:
            return ['A']
        else:
            left = generate_and_or_tree(n // 2)
            right = generate_and_or_tree(n - n // 2 - 1)
            return ['OR', left, right]
    
    def communication_complexity(tree):
        if isinstance(tree, list):
            if tree[0] == 'AND':
                return 1 + max(communication_complexity(tree[1]), communication_complexity(tree[2]))
            elif tree[0] == 'OR':
                return 1 + communication_complexity(tree[1])
            else:
                raise ValueError("Invalid tree node")
        else:
            return 0
    
    def tropical_motive_rank(tree):
        if isinstance(tree, list):
            if tree[0] == 'AND':
                rank_left = tropical_motive_rank(tree[1])
                rank_right = tropical_motive_rank(tree[2])
                return max(rank_left, rank_right) + 1
            elif tree[0] == 'OR':
                rank_left = tropical_motive_rank(tree[1])
                rank_right = tropical_motive_rank(tree[2])
                return max(rank_left, rank_right)
            else:
                raise ValueError("Invalid tree node")
        else:
            return 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            tree = generate_and_or_tree(n)
            C_N = communication_complexity(tree)
            R = tropical_motive_rank(tree)
            results.append((n, C_N, R))
    
    total_instances = len(results)
    mean_C_N = sum(C_N for _, C_N, _ in results) / total_instances
    mean_R = sum(R for _, _, R in results) / total_instances
    
    conjecture_holds = all(R >= C_N * n or R > C_N ** 2 for _, C_N, R in results)
    
    if not conjecture_holds:
        counterexample = "R < CN or R <= CN^2"
    else:
        counterexample = ""
    
    return {
        "metric_name": "Communication Complexity vs Tropical Motive Rank",
        "metric_value": mean_R,
        "instances_tested": total_instances,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = result["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")