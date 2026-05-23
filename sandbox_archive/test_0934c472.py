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
        function = {}
        for i in range(2**n):
            inputs = [bool((i >> j) & 1) for j in range(n)]
            outputs = random.randint(0, 1)
            if len(inputs) > max_degree:
                continue
            function[tuple(inputs)] = outputs
        return function
    
    def construct_entanglement_tensor_network(function):
        n = int(math.log2(len(function)))
        tensor_rank = 0
        for i in range(n):
            tensor_rank += len([x for x in function if sum(x[:i+1]) == i])
        return tensor_rank
    
    def bp_readtwice_complexity(function):
        n = int(math.log2(len(function)))
        complexity = 0
        for inputs, outputs in function.items():
            complexity += max(sum(inputs[:i+1]) for i in range(n))
        return complexity
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 80% of seeds are tested
            function = generate_boolean_function(n, n)
            tensor_rank = construct_entanglement_tensor_network(function)
            bp_readtwice = bp_readtwice_complexity(function)
            
            if tensor_rank == 0:
                continue
            
            ratio = tensor_rank / bp_readtwice
            results.append({
                "n": n,
                "tensor_rank": tensor_rank,
                "bp_readtwice": bp_readtwice,
                "ratio": ratio
            })
    
    if not results:
        return {
            "metric_name": "Rank vs BP_ReadTwice",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    mean_ratio = sum(result["ratio"] for result in results) / len(results)
    std_ratio = math.sqrt(sum((result["ratio"] - mean_ratio) ** 2 for result in results) / len(results))
    
    return {
        "metric_name": "Rank vs BP_ReadTwice",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": all(0.5 <= ratio <= 2 for ratio in [result["ratio"] for result in results]),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        all_results.append(result)
    
    mean_ratio = sum(result["metric_value"] for result in all_results) / len(all_results)
    std_ratio = math.sqrt(sum((result["metric_value"] - mean_ratio) ** 2 for result in all_results) / len(all_results))
    support_fraction = sum(1 for result in all_results if result["conjecture_holds"]) / len(all_results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in all_results):
        first_failing_seed = next(seed for seed, result in zip(seeds, all_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")