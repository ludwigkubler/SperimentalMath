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
    
    def generate_boolean_function(n, max_degree):
        function = []
        for _ in range(2**n):
            inputs = [random.randint(0, 1) for _ in range(n)]
            output = random.choice([0, 1])
            if len(set(inputs)) <= max_degree:
                function.append((inputs, output))
        return function

    def construct_entanglement_tensor_network(function):
        # Simplified construction for demonstration
        rank = len(function)
        return rank

    def bp_readtwice_complexity(rank, n):
        # Simplified complexity calculation for demonstration
        return rank * n

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        max_degree = min(n, 10)  # Limiting max degree to avoid trivial cases
        function = generate_boolean_function(n, max_degree)
        rank = construct_entanglement_tensor_network(function)
        complexity = bp_readtwice_complexity(rank, n)
        
        if complexity == 0:
            continue
        
        ratio = rank / max_degree
        results.append({
            "n": n,
            "max_degree": max_degree,
            "rank": rank,
            "complexity": complexity,
            "ratio": ratio
        })
    
    if not results:
        return {
            "metric_name": "Rank vs BP_ReadTwice",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    mean_ratio = sum(result["ratio"] for result in results) / len(results)
    std_ratio = math.sqrt(sum((result["ratio"] - mean_ratio)**2 for result in results) / len(results))
    
    conjecture_holds = all(0.5 <= ratio <= 1.5 for result in results)
    counterexample = "" if conjecture_holds else "Ratio outside [0.5, 1.5] range"
    
    return {
        "metric_name": "Rank vs BP_ReadTwice",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
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
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    std_ratio = math.sqrt(sum((result["metric_value"] - mean_ratio)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio outside [0.5, 1.5] range\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")