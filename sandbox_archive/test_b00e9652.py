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
    
    def generate_boolean_function(n, max_degree):
        function = []
        for _ in range(n):
            degree = random.randint(1, max_degree)
            variables = sorted(random.sample(range(n), degree))
            function.append((variables, random.choice([0, 1])))
        return function
    
    def evaluate_function(function, assignment):
        result = 0
        for (vars, val) in function:
            product = 1
            for var in vars:
                product *= assignment[var]
            result += val * product
        return result % 2
    
    def construct_entanglement_tensor_network(function):
        n = len(function)
        rank = 0
        # Simplified construction using a dictionary to represent the network
        tensor = {}
        for (vars, val) in function:
            key = tuple(sorted(vars))
            if key not in tensor:
                tensor[key] = []
                rank += 1
            tensor[key].append(val)
        return tensor, rank
    
    def compute_delta(f):
        return max(len(vars) for vars, _ in f)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        delta_max = n
        function = generate_boolean_function(n, delta_max)
        tensor, rank = construct_entanglement_tensor_network(function)
        
        if rank == 0 or delta_max == 0:
            continue
        
        ratio = Fraction(rank, delta_max).limit_denominator()
        results.append({"n": n, "rank": rank, "delta": delta_max, "ratio": ratio})
    
    mean_ratio = sum(result["ratio"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["ratio"] == mean_ratio) / len(results)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Rank vs Delta",
        "metric_value": float(mean_ratio),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    total_trials = len(seeds)
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / total_trials
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / total_trials
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")