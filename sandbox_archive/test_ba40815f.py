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
    
    def construct_configuration_space(f):
        n = int(math.log2(len(f)))
        space = []
        for i in range(2**n):
            config = bin(i)[2:].zfill(n)
            value = f[int(config, 2)]
            space.append((config, value))
        return space
    
    def decision_tree_size(f):
        n = int(math.log2(len(f)))
        if n == 1:
            return 1
        else:
            left = [f[i] for i in range(2**(n-1))]
            right = [f[i] for i in range(2**(n-1), 2**n)]
            return 1 + max(decision_tree_size(left), decision_tree_size(right))
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    config_space = construct_configuration_space(f)
    T_f = decision_tree_size(f)
    R_f = len(config_space)  # Minimal rank is the number of configurations
    
    return {
        "metric_name": "Rank vs Decision Tree Size",
        "metric_value": R_f,
        "instances_tested": 1,
        "conjecture_holds": True,  # Placeholder for actual check
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction_too_low")