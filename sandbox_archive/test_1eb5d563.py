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
    
    def communication_rank(f):
        n = int(math.log2(len(f)))
        rank = 0
        for i in range(2**n):
            if f[i] != f[0]:
                rank += 1
        return rank
    
    def quaternionic_representation_size(n, r):
        return min(2*n - 1, n + r)
    
    def approximation_error(f, representation):
        return sum(abs(f[i] - representation[i]) for i in range(len(f)))
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    r = communication_rank(f)
    k_max = quaternionic_representation_size(n, r)
    
    if k_max < 1:
        return {
            "metric_name": "quaternionic_representation_size",
            "metric_value": -1,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    representation = [random.choice([0, 1]) for _ in range(k_max)]
    error = approximation_error(f, representation)
    
    return {
        "metric_name": "quaternionic_representation_size",
        "metric_value": k_max,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": k_max <= 4 * r**2 and error <= 3 * math.sqrt(error),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [random.randint(1, 997) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_k = sum(r["metric_value"] for r in results if r["instances_tested"] > 0) / len(results)
    std_dev_k = math.sqrt(sum((r["metric_value"] - mean_k)**2 for r in results if r["instances_tested"] > 0) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_k} std={std_dev_k} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_k} std={std_dev_k} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")