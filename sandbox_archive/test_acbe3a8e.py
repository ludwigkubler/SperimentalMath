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

def generate_random_boolean_function(n):
    return [random.randint(0, 1) for _ in range(2**n)]

def symplectic_leaves(f):
    n = int(math.log2(len(f)))
    leaves = set()
    for i in range(2**n):
        leaf = tuple(f[i:i+n])
        if leaf not in leaves:
            leaves.add(leaf)
    return len(leaves)

def randomized_two_party_communication_complexity(f):
    n = int(math.log2(len(f)))
    complexity = 0
    for _ in range(10):  # Sample 10 random inputs to estimate the complexity
        input_index = random.randint(0, len(f) - 1)
        input_bits = [int(bit) for bit in bin(input_index)[2:].zfill(n)]
        output_bit = f[input_index]
        complexity += sum(input_bits) + output_bit
    return complexity / (n + 1)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        L_f = symplectic_leaves(f)
        CC_R_f = randomized_two_party_communication_complexity(f)
        
        if L_f > n:  # Upper bound g(n) is n
            return {
                "metric_name": "CC_R(f)",
                "metric_value": CC_R_f,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"Function with {n} inputs and {L_f} leaves"
            }
    
    return {
        "metric_name": "CC_R(f)",
        "metric_value": sum(CC_R_f for _ in range(30)) / 30,  # Average over multiple samples
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Function with {result['n_max']} inputs and {result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")