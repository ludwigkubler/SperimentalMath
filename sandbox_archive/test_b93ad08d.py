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
    
    def generate_random_function(n, d):
        if n == 1:
            return [random.choice([0, 1])]
        else:
            functions = []
            for _ in range(d):
                sub_functions = [generate_random_function(n-1, d) for _ in range(2)]
                functions.append(sub_functions)
            return functions
    
    def tropicalize(f):
        if isinstance(f, list):
            result = []
            for sub_f in f:
                sub_result = tropicalize(sub_f)
                result.extend(sub_result)
            return result
        else:
            return [f]
    
    def rank(tropicalized_function):
        # Simple heuristic to estimate the rank
        return len(set(tropicalized_function))
    
    n = random.randint(5, 40)
    d = random.randint(1, 3)
    f = generate_random_function(n, d)
    tropicalized_f = tropicalize(f)
    rho_f = rank(tropicalized_f)
    
    metric_name = "minimal_rank"
    metric_value = rho_f
    instances_tested = 1
    conjecture_holds = rho_f >= d * math.log(n)
    counterexample = "" if conjecture_holds else f"n={n}, d={d}, rho(f)={rho_f}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")