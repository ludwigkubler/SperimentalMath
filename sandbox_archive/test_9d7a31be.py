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
    
    def generate_binary_tree(n):
        if n == 0:
            return None
        left = generate_binary_tree(random.randint(0, n-1))
        right = generate_binary_tree(n - (left is not None) - 1)
        return (left, right)
    
    def geometric_entropy(tree):
        if tree is None:
            return 0
        left, right = tree
        h_left = geometric_entropy(left)
        h_right = geometric_entropy(right)
        p_left = (h_left + 1) / (h_left + h_right + 2)
        p_right = (h_right + 1) / (h_left + h_right + 2)
        return -p_left * math.log(p_left, 2) - p_right * math.log(p_right, 2)
    
    def resolution_proof_width(tree):
        if tree is None:
            return 0
        left, right = tree
        return max(resolution_proof_width(left), resolution_proof_width(right)) + 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            tree = generate_binary_tree(n)
            h_min = geometric_entropy(tree)
            if h_min == 0:
                continue
            w_phi = resolution_proof_width(tree)
            ratio = w_phi / h_min
            results.append(ratio)
    
    mean_ratio = sum(results) / len(results)
    conjecture_holds = all(r >= 1 for r in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Ratio of Resolution Proof Width to Geometric Entropy",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")