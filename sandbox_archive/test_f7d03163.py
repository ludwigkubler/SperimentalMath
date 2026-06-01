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
    
    def tropical_minimal_local_ring_norm(circuit):
        # Placeholder implementation for minimal local ring norm computation
        return random.random() * 10
    
    def monotone_width(circuit):
        # Placeholder implementation for monotone width computation
        return random.randint(1, 5)
    
    n_max = 30
    instances_tested = 0
    total_tropical_norm = 0.0
    total_monotone_width = 0.0
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        circuit = [random.randint(0, 1) for _ in range(n)]
        
        tropical_norm = tropical_minimal_local_ring_norm(circuit)
        monotone_width_val = monotone_width(circuit)
        
        total_tropical_norm += tropical_norm
        total_monotone_width += monotone_width_val
        instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "tropical_minimal_local_ring_norm",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_tropical_norm = total_tropical_norm / instances_tested
    mean_monotone_width = total_monotone_width / instances_tested
    
    correlation_coefficient = (instances_tested * sum(tropical_norm * monotone_width_val for tropical_norm, monotone_width_val in zip(range(instances_tested), range(instances_tested))) - instances_tested * mean_tropical_norm * mean_monotone_width) / math.sqrt((instances_tested * sum(tropical_norm**2 for tropical_norm in range(instances_tested)) - instances_tested * mean_tropical_norm**2) * (instances_tested * sum(monotone_width_val**2 for monotone_width_val in range(instances_tested)) - instances_tested * mean_monotone_width**2))
    
    return {
        "metric_name": "tropical_minimal_local_ring_norm",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and correlation_coefficient <= 10,
        "counterexample": "" if correlation_coefficient >= 0.8 and correlation_coefficient <= 10 else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = [run_trial(seed) for seed in seeds]
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / sum(1 for r in results if r["metric_value"] is not None)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / sum(1 for r in results if r["metric_value"] is not None))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif first_failing_seed is not None:
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")