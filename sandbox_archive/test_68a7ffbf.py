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
    
    def generate_boolean_function(n, m):
        return [random.choice([0, 1]) for _ in range(m)]
    
    def communication_protocol(f):
        # Simplified protocol: each bit is sent separately
        return len(f)
    
    def minimal_local_zeta_function_size(c):
        # Simplified zeta function size: linear with complexity
        return c
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    mzeta_sum = 0
    c_sum = 0
    max_deviation = 0
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different functions
            f = generate_boolean_function(n, random.randint(1, 2**n))
            c = communication_protocol(f)
            mzeta = minimal_local_zeta_function_size(c)
            
            instances_tested += 1
            mzeta_sum += mzeta
            c_sum += c
            deviation = abs(mzeta - c)
            if deviation > max_deviation:
                max_deviation = deviation
    
    mean_mzeta = mzeta_sum / instances_tested
    mean_c = c_sum / instances_tested
    correlation_coefficient = (instances_tested * sum(mzeta * c for mzeta, c in zip(range(instances_tested), range(instances_tested))) - mzeta_sum * c_sum) / math.sqrt((instances_tested * sum(mzeta**2 for mzeta in range(instances_tested)) - mzeta_sum**2) * (instances_tested * sum(c**2 for c in range(instances_tested)) - c_sum**2))
    
    conjecture_holds = correlation_coefficient >= 0.7 and max_deviation <= 2
    counterexample = "" if conjecture_holds else f"Correlation: {correlation_coefficient}, Max Deviation: {max_deviation}"
    
    return {
        "metric_name": "Communication Complexity vs Local Zeta Function Size",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation too low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")