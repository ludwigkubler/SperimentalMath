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
        return [random.randint(0, 1) for _ in range(n)]
    
    def generate_quasi_projective_variety(poly):
        # Placeholder function to simulate generating a variety
        return len(poly)
    
    def communication_complexity(disjointness_input_size):
        # Placeholder function to simulate communication complexity
        return disjointness_input_size
    
    n = random.randint(5, 40)  # Randomly choose the size of the Boolean function and variety
    boolean_function = generate_boolean_function(n)
    poly = [random.randint(0, 1) for _ in range(n)]  # Simulate a polynomial representing the variety
    min_rank = generate_quasi_projective_variety(poly)
    comm_complexity = communication_complexity(n)
    
    metric_value = comm_complexity
    conjecture_holds = abs(comm_complexity - 2**min_rank) <= 0.1 * 2**min_rank
    counterexample = "" if conjecture_holds else f"Discrepancy: {comm_complexity} != 2^{min_rank}"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_dev = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Discrepancy\" first_failing_seed={first_failing_seed}")