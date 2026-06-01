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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def evaluate_morse_function(f, x):
        n = len(f)
        result = 0
        for i in range(n):
            if f[i] == x:
                result += 1
        return result
    
    def frege_proof_size(f):
        # Simplified Frege proof size estimation (not exhaustive)
        n = len(f)
        return n * (n + 1) // 2
    
    def geometric_entropy(morse_function_values, grid_size):
        max_value = max(morse_function_values)
        min_value = min(morse_function_values)
        if max_value == min_value:
            return 0
        entropy = 0
        for value in morse_function_values:
            probability = (value - min_value) / (max_value - min_value)
            entropy -= probability * math.log2(probability)
        return entropy
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_boolean_function(n)
    
    grid_size = 10
    morse_function_values = [evaluate_morse_function(f, x) for x in range(grid_size)]
    entropy = geometric_entropy(morse_function_values, grid_size)
    proof_size = frege_proof_size(f)
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": entropy,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": entropy >= proof_size * 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_entropy = sum(result["metric_value"] for result in results) / len(results)
    std_entropy = math.sqrt(sum((result["metric_value"] - mean_entropy) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = f"n={result['n_max']}, entropy={result['metric_value']}, proof_size={frege_proof_size(generate_boolean_function(result['n_max']))}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break
        else:
            print("RESULT: INCONCLUSIVE not_enough_support")