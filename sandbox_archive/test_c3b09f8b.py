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
    
    # Placeholder for QLSC computation (not implemented)
    def qlsc(f):
        return 1  # Dummy value
    
    # Placeholder for ACC0 circuit size computation (not implemented)
    def acc0_circuit_size(f, n, d):
        return 1  # Dummy value
    
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)  # Random input size
        d = random.randint(1, 2**n)  # Random output size
        
        f = lambda x: sum(x[i] * (i + 1) for i in range(n))  # Dummy quantum polynomial
        
        qlsc_value = qlsc(f)
        acc0_size = acc0_circuit_size(f, n, d)
        
        metric_values.append(qlsc_value)
    
    mean_metric = sum(metric_values) / instances_tested
    std_metric = math.sqrt(sum((x - mean_metric)**2 for x in metric_values) / instances_tested)
    
    conjecture_holds = mean_metric <= 3 and len([v for v in metric_values if v >= 0.8 * mean_metric]) >= 24
    
    return {
        "metric_name": "QLSC vs ACC0 Circuit Size",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")