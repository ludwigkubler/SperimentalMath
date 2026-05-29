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

def generate_random_boolean_function(n):
    return [random.randint(0, 1) for _ in range(2**n)]

def symplectic_leaves(f):
    n = int(math.log2(len(f)))
    leaves = set()
    for i in range(2**n):
        leaf = tuple(f[i])
        if leaf not in leaves:
            leaves.add(leaf)
    return len(leaves)

def randomized_two_party_communication_complexity(f):
    n = int(math.log2(len(f)))
    max_bits_sent = 0
    for _ in range(100):  # Sample 100 random inputs to estimate communication complexity
        x = random.randint(0, 2**n - 1)
        y = f[x]
        bits_sent = bin(x).count('1')
        if bits_sent > max_bits_sent:
            max_bits_sent = bits_sent
    return max_bits_sent

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        L_f = symplectic_leaves(f)
        CC_R_f = randomized_two_party_communication_complexity(f)
        
        if L_f > n:  # Upper bound g(n) is n (trivial case)
            return {
                "metric_name": "CC_R(f)",
                "metric_value": CC_R_f,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"Counterexample for n={n}: L(f) = {L_f} > g(n) = {n}"
            }
        
        results.append(CC_R_f)
    
    mean_CC_R = sum(results) / len(results)
    std_CC_R = math.sqrt(sum((x - mean_CC_R)**2 for x in results) / len(results))
    
    return {
        "metric_name": "CC_R(f)",
        "metric_value": mean_CC_R,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean_val = sum(results) / len(results)
    std_val = math.sqrt(sum((x - mean_val)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= 0) / len(results)
    
    if all(r <= 0 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_val} std={std_val} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_val} std={std_val} support_fraction={support_fraction}")
    else:
        first_failing_seed = seeds[next(i for i, r in enumerate(results) if r > 0)]
        print(f"RESULT: FALSIFIED counterexample='CC_R(f) > 0' first_failing_seed={first_failing_seed}")