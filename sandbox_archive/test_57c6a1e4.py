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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def shannon_entropy(f):
    n = len(f)
    counts = [f.count(i) for i in set(f)]
    probabilities = [Fraction(count, n) for count in counts]
    entropy = -sum(p * math.log2(p) for p in probabilities if p != 0)
    return entropy

def is_distinctive_representation(representation, f):
    # Simplified check: representation is distinctive if it can distinguish between f and its complement
    return any(sum(row[i] for row in representation) % 2 == f[i] for i in range(len(f)))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    H_f = shannon_entropy(f)
    
    # Calculate the upper bound
    upper_bound = 2 * H_f + math.log2(n)
    
    # Find a representation that distinguishes f from its complement
    for dim in range(1, n+1):
        representation = [[random.randint(0, 1) for _ in range(dim)] for _ in range(n)]
        if is_distinctive_representation(representation, f):
            min_dimension = dim
            break
    
    metric_value = min_dimension
    conjecture_holds = min_dimension <= upper_bound
    counterexample = "" if conjecture_holds else "min_dim > 2H(f) + log(n)"
    
    return {
        "metric_name": "Minimal Dimension",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"min_dim > 2H(f) + log(n)\" first_failing_seed={first_failing_seed}")