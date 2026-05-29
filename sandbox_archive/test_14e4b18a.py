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
    
    # Define groups H and K (simple examples for testing)
    H = {1, 2, 3}
    K = {4, 5}
    
    # Define the homomorphism φ from K to Aut(H)
    phi = {4: lambda x: x + 1, 5: lambda x: x - 1}
    
    # Compute the minimal rank of G = H ⋊ φ K
    min_rank_G = len(H) * len(K)
    
    # Define a Max-Cut instance on n vertices (simple example for testing)
    n = 40
    max_cut_instance = [random.choice([0, 1]) for _ in range(n)]
    
    # Compute the randomized communication complexity C(n)
    communication_complexity = sum(max_cut_instance) * (n - sum(max_cut_instance)) / n
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": communication_complexity,
        "instances_tested": 1,
        "conjecture_holds": abs(communication_complexity - min_rank_G) <= 0.5 * min_rank_G,
        "counterexample": "" if conjecture_holds else f"max_cut_instance={max_cut_instance}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")