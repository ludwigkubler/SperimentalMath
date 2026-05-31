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

# Khinchin's constant K_2 ≈ 0.41421356237309504
K_2 = 0.41421356237309504

def communication_complexity(f):
    # Generate a random input vector of length n
    n = len(f)
    x = [random.choice([0, 1]) for _ in range(n)]
    
    # Evaluate the function on the input vector
    y = f(x)
    
    # Calculate the communication complexity
    CC_f = sum(1 if xi != yi else 0 for xi, yi in zip(x, y))
    
    return CC_f

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    metric_name = "communication_complexity"
    instances_tested = 30
    n_max = 40
    conjecture_holds = True
    counterexample = ""
    
    total_CC_f = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Generate 5 instances per size
            f = lambda x: [x[i] ^ x[(i + 1) % n] for i in range(n)]
            CC_f = communication_complexity(f)
            total_CC_f += CC_f
    
    mean_CC_f = total_CC_f / (instances_tested * n_max)
    ratio = mean_CC_f / (K_2 ** (n_max - 1))
    
    if abs(ratio - 1) > 0.05:
        conjecture_holds = False
        counterexample = f"Ratio {ratio} outside ±5% of 1"
    
    return {
        "metric_name": metric_name,
        "metric_value": mean_CC_f,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")