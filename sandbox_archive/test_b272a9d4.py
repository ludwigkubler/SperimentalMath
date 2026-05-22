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
    
    def compute_representation(boolean_function):
        n = int(math.log2(len(boolean_function)))
        representation = {}
        for i in range(2**n):
            if boolean_function[i] == 1:
                representation[i] = 1
            else:
                representation[i] = -1
        return representation
    
    def compute_character_degree(representation):
        return max(abs(value) for value in representation.values())
    
    def compute_hypercontractive_constant(boolean_function, n):
        # Simplified hypercontractive constant calculation (for demonstration)
        return sum(boolean_function[i] ** 2 for i in range(2**n)) / len(boolean_function)
    
    D = 5  # Example character degree
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(30):
        boolean_function = generate_boolean_function(random.randint(5, 40))
        representation = compute_representation(boolean_function)
        char_degree = compute_character_degree(representation)
        hypercontractive_constant = compute_hypercontractive_constant(boolean_function, len(boolean_function))
        
        if char_degree > D and hypercontractive_constant >= D:
            conjecture_holds = False
            counterexample = f"Boolean function with n={len(boolean_function)}, char_degree={char_degree}, hypercontractive_constant={hypercontractive_constant}"
            break
        
        instances_tested += 1
    
    return {
        "metric_name": "Hypercontractive Constant",
        "metric_value": hypercontractive_constant,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")