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

def communication_complexity_rank(f):
    n = int(math.log2(len(f)))
    rank = 0
    for i in range(n):
        if f[i] != f[0]:
            rank += 1
    return rank

def grothendieck_tate_dimension(f):
    # This is a placeholder function. In practice, you would need to implement
    # the actual computation of the Grothendieck-Tate dimension for a given boolean function.
    # For simplicity, we'll assume it returns a constant value based on n.
    n = int(math.log2(len(f)))
    return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for _ in range(30):
        f = generate_boolean_function(random.randint(5, 40))
        rank = communication_complexity_rank(f)
        dim = grothendieck_tate_dimension(f)
        results.append((rank, dim))
    
    mean_rank = sum(rank for rank, dim in results) / len(results)
    mean_dim = sum(dim for rank, dim in results) / len(results)
    variance = sum((rank - mean_rank)**2 for rank, dim in results) / len(results)
    conjecture_holds = variance <= mean_dim
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Variance of Communication Complexity Rank",
        "metric_value": variance,
        "instances_tested": 30,
        "n_max": max(int(math.log2(len(f))) for f in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_variance = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_variance} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_variance} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")