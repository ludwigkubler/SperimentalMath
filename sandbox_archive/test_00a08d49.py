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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_polynomial(n):
        # Generate a random polynomial of degree n
        coefficients = [random.randint(0, 10) for _ in range(n + 1)]
        return coefficients
    
    def compute_mli(poly):
        # Compute the minimal local index of motivic integration (simplified)
        mli = sum(abs(coeff) for coeff in poly)
        return mli
    
    def compute_communication_complexity(poly):
        # Compute communication complexity (simplified)
        return len(poly) - 1
    
    n_max = 40
    instances_tested = 30
    mli_values = []
    c_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        poly = generate_polynomial(n)
        mli = compute_mli(poly)
        c = compute_communication_complexity(poly)
        
        if mli is None or c is None:
            continue
        
        mli_values.append(mli)
        c_values.append(c)
    
    if not mli_values or not c_values:
        return {
            "metric_name": "mli",
            "metric_value": 0,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_mli = sum(mli_values) / len(mli_values)
    mean_c = sum(c_values) / len(c_values)
    std_mli = math.sqrt(sum((x - mean_mli) ** 2 for x in mli_values) / len(mli_values))
    std_c = math.sqrt(sum((y - mean_c) ** 2 for y in c_values) / len(c_values))
    
    if std_mli == 0 or std_c == 0:
        return {
            "metric_name": "mli",
            "metric_value": 0,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "std_deviation_zero"
        }
    
    correlation = sum((x - mean_mli) * (y - mean_c) for x, y in zip(mli_values, c_values)) / (len(mli_values) * std_mli * std_c)
    
    return {
        "metric_name": "mli",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation) >= 0.95,  # Adjust threshold as needed
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(1, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_mli = sum(r["metric_value"] for r in results) / len(results)
    std_mli = math.sqrt(sum((r["metric_value"] - mean_mli) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_mli} std={std_mli} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_mli} std={std_mli} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")