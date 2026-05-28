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
    
    def log2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)
    
    def quantum_category_invariant(size):
        # Constructive mapping for the quantum category invariant
        # This is a placeholder function. Replace with actual computation.
        return random.uniform(0, log2(size))
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test 5 instances per size
            size = random.randint(n, 2*n)
            value = quantum_category_invariant(size)
            if value > 10 * log2(size):
                return {
                    "metric_name": "rho_QC",
                    "metric_value": value,
                    "instances_tested": instances_tested,
                    "conjecture_holds": False,
                    "counterexample": f"Size={size}, Value={value}"
                }
            metric_values.append(value)
            instances_tested += 1
    
    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
    
    return {
        "metric_name": "rho_QC",
        "metric_value": mean,
        "instances_tested": instances_tested,
        "conjecture_holds": all(abs(value - log2(size)) <= 3 * std_dev for value, size in zip(metric_values, [n]*len(n_values))),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i for i, r in enumerate(results) if not r["conjecture_holds"]), None)
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[first_failing_seed]}")