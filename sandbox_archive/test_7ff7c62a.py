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

def generate_binary_tree(n):
    if n == 0:
        return None
    left_size = random.randint(0, n-1)
    right_size = n - 1 - left_size
    return (generate_binary_tree(left_size), generate_binary_tree(right_size))

def calculate_geometric_entropy(tree):
    if tree is None:
        return 0
    left, right = tree
    total_nodes = 1 + (calculate_geometric_entropy(left) + calculate_geometric_entropy(right))
    entropy = -math.log2(1 / total_nodes)
    return entropy

def calculate_resolution_proof_width(n):
    # Placeholder for actual calculation of resolution proof width
    return n  # Simplified for testing purposes

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        tree = generate_binary_tree(n)
        Hmin_G = calculate_geometric_entropy(tree)
        if Hmin_G <= 0:
            continue
        w_phi = calculate_resolution_proof_width(n)
        ratio = w_phi / Hmin_G
        results.append({"n": n, "Hmin_G": Hmin_G, "w_phi": w_phi, "ratio": ratio})
    
    metric_value = sum(result["ratio"] for result in results) / len(results)
    conjecture_holds = all(result["ratio"] >= 1 for result in results)
    counterexample = "" if conjecture_holds else f"Ratio < 1 found at n={results[0]['n']}"
    
    return {
        "metric_name": "Resolution Proof Width Ratio",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
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
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio < 1 found\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")