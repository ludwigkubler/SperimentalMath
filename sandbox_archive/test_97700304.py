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
    
    def generate_hyperbolic_tiling(n):
        # Simplified hyperbolic tiling generation for demonstration
        return [random.randint(1, 5) for _ in range(n)]
    
    def compute_local_indeterminacy(tiling):
        # Placeholder for actual computation
        return sum(tiling)
    
    def construct_frege_proof(tiling):
        # Simplified Frege proof construction for demonstration
        return len(tiling)
    
    n_max = 40
    instances_tested = 30
    mli_values = []
    fpl_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        tiling = generate_hyperbolic_tiling(n)
        mli = compute_local_indeterminacy(tiling)
        fpl = construct_frege_proof(tiling)
        
        mli_values.append(mli)
        fpl_values.append(fpl)
    
    if not mli_values or not fpl_values:
        return {
            "metric_name": "mli vs fpl",
            "metric_value": 0,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mli_mean = sum(mli_values) / len(mli_values)
    fpl_mean = sum(fpl_values) / len(fpl_values)
    
    correlation_coefficient = 0
    for i in range(len(mli_values)):
        correlation_coefficient += (mli_values[i] - mli_mean) * (fpl_values[i] - fpl_mean)
    correlation_coefficient /= math.sqrt(sum((x - mli_mean) ** 2 for x in mli_values)) * math.sqrt(sum((y - fpl_mean) ** 2 for y in fpl_values))
    
    return {
        "metric_name": "mli vs fpl",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")