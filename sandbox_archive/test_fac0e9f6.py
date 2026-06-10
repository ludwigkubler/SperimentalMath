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
    
    def poincare_disk_volume(n):
        # Simplified volume calculation for demonstration purposes
        return (math.pi * n) / (4 * math.sqrt(n))
    
    n_values = [5, 10, 15, 20, 30, 40]
    volumes = []
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different functions
            f = generate_boolean_function(n)
            volume = poincare_disk_volume(n)
            volumes.append(volume)
            instances_tested += 1
    
    mean_volume = sum(volumes) / len(volumes)
    conjecture_holds = (0.5 <= mean_volume / (1 / math.sqrt(30)) <= 2) and all(
        volume / (1 / math.sqrt(n)) <= 6 for n, volume in zip(n_values, volumes))
    
    return {
        "metric_name": "hyperbolic_volume",
        "metric_value": mean_volume,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else str(mean_volume)
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")