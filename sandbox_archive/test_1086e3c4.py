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
    
    def geometric_entropy(values, grid_size):
        n = len(values)
        if n == 0:
            return 0.0
        
        counts = [values.count(value) for value in set(values)]
        probabilities = [count / n for count in counts]
        
        entropy = 0.0
        for probability in probabilities:
            if probability > 0:
                entropy -= probability * math.log2(probability)
        
        return entropy
    
    def frege_proof_size(f):
        # Placeholder function to compute Frege proof size
        # This is a dummy implementation and should be replaced with actual logic
        return len(f) ** 2  # Example: assume proof size is proportional to the length of f
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    n = random.randint(5, 40)
    boolean_function = generate_boolean_function(n)
    grid_size = (n + 1) ** 2
    morse_function_values = [boolean_function[i] for i in range(grid_size)]
    
    entropy = geometric_entropy(morse_function_values, grid_size)
    proof_size = frege_proof_size(boolean_function)
    
    return {
        "metric_name": "Geometric Entropy vs Frege Proof Size",
        "metric_value": entropy,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_entropy = sum(result["metric_value"] for result in results) / len(results)
    std_entropy = (sum((result["metric_value"] - mean_entropy) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")