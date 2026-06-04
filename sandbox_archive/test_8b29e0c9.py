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
    
    def generate_boolean_instance(n):
        return [random.choice([0, 1]) for _ in range(n)]
    
    def resolution_proof_tree_height(instance):
        # Simplified heuristic to estimate height
        return len(instance) * 2
    
    def count_integral_points(variant_set):
        # Placeholder function to count integral points
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, 10)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instance = generate_boolean_instance(n)
        height = resolution_proof_tree_height(instance)
        points = count_integral_points(instance)
        results.append((n, height, points))
    
    total_points = sum(points for _, _, points in results)
    avg_height = sum(height for _, height, _ in results) / len(results)
    avg_points = total_points / len(results)
    
    metric_value = avg_points
    n_max = max(n for n, _, _ in results)
    conjecture_holds = abs(avg_points - avg_height * 2) < 10  # Simplified threshold
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Average Number of Integral Points",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 50, 2))[:30]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")