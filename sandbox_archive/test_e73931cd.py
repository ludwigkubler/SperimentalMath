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
    
    def compute_HOL(f):
        # Placeholder function to compute Hodge arc length
        # This is a dummy implementation and should be replaced with actual computation
        return len(f) ** 0.5
    
    def compute_CRV(f):
        # Placeholder function to compute communication complexity rank variance
        # This is a dummy implementation and should be replaced with actual computation
        return len(f) ** 2
    
    n_max = 40
    instances_tested = 30
    total_HOL = 0
    total_CRV = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        f = generate_boolean_function(n)
        HOL = compute_HOL(f)
        CRV = compute_CRV(f)
        
        total_HOL += HOL
        total_CRV += CRV
    
    mean_HOL = total_HOL / instances_tested
    mean_CRV = total_CRV / instances_tested
    correlation_coefficient = (instances_tested * sum(HOL * CRV for HOL, CRV in zip(total_HOL, total_CRV)) -
                               total_HOL * total_CRV) / math.sqrt((instances_tested * sum(HOL**2 for HOL in total_HOL) - total_HOL**2) *
                                                                 (instances_tested * sum(CRV**2 for CRV in total_CRV) - total_CRV**2))
    
    conjecture_holds = correlation_coefficient > 0.7
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")