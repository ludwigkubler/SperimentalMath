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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        count = 0
        for i in range(2**n):
            if f[i] != f[~i]:
                count += 1
        return count
    
    def symplectic_leaves_number(f):
        n = int(math.log2(len(f)))
        leaves = set()
        for i in range(2**n):
            leaf = tuple(f[j] for j in range(n) if (i >> j) & 1)
            leaves.add(leaf)
        return len(leaves)
    
    def log_2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        L_f = symplectic_leaves_number(f)
        CC_R_f = communication_complexity(f)
        
        if L_f > n:  # Upper bound g(n) is n
            conjecture_holds = False
            counterexample = "L(f) > n"
        else:
            conjecture_holds = True
            counterexample = ""
        
        results.append({
            "metric_name": "CC_R(f)",
            "metric_value": CC_R_f,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_metric_value": mean_metric_value,
        "std_metric_value": std_metric_value,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["mean_metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["mean_metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["support_fraction"] >= 0.8) / len(results)
    
    if support_fraction == 1:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(result["support_fraction"] < 0.8 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["support_fraction"] < 0.8)
        print(f"RESULT: FALSIFIED counterexample=\"L(f) > n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")