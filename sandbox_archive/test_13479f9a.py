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
    
    def bp_read_twice_circuit_size(f):
        n = int(math.log2(len(f)))
        # Simplified model of BP_read_twice circuit size
        return 2 * n + 3
    
    def entropic_complexity(f):
        # Simplified entropy calculation (logarithm base 2)
        return math.log2(1 / sum(1 for x in f if x == 0) + 1)
    
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.randint(5, 40)
        f = generate_boolean_function(n)
        s = bp_read_twice_circuit_size(f)
        E_f = entropic_complexity(f)
        
        if not (1 <= E_f <= math.log2(s + 1)):
            return {
                "metric_name": "Entropic Complexity vs BP ReadTwice Circuit Size",
                "metric_value": E_f,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, s={s}, E(f)={E_f}"
            }
        
        results.append(E_f)
    
    return {
        "metric_name": "Entropic Complexity vs BP ReadTwice Circuit Size",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 1 and r <= math.log2(s + 1)) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r < 1 or r > math.log2(s + 1) for r in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not (1 <= result <= math.log2(s + 1)))
        print(f"RESULT: FALSIFIED counterexample=\"out of range\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")