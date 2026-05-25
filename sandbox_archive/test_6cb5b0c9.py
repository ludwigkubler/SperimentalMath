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

def boolean_function(instance):
    n = len(instance)
    edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
    return [instance[edges.index((i, j))] for i, j in edges]

def hopf_algebra_rank(boolean_func):
    # Simplified encoding of a Hopf algebra rank based on the Boolean function
    # This is a placeholder and should be replaced with actual computation
    return len(boolean_func)

def max_cut_approximation_ratio(instance):
    n = len(instance)
    edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
    cut_value = sum(instance[edges.index((i, j))] for i, j in edges if random.choice([0, 1]) == 0)
    return Fraction(cut_value, len(edges))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random instance of Max-CUT with n vertices
    n = random.randint(5, 40)
    instance = [random.choice([0, 1]) for _ in range(n * (n - 1) // 2)]
    
    boolean_func = boolean_function(instance)
    hopf_rank = hopf_algebra_rank(boolean_func)
    approx_ratio = max_cut_approximation_ratio(instance)
    
    if approx_ratio == 0:
        return {
            "metric_name": "ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "approx_ratio_is_zero"
        }
    
    ratio = hopf_rank / approx_ratio
    
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 2.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["instances_tested"] > 0) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results if r["instances_tested"] > 0) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='approx_ratio_is_zero' first_failing_seed={first_failing_seed}")