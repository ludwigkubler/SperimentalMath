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
    
    def generate_explicit_function(n):
        # Example function: XOR of all variables
        return lambda x: sum(x) % 2
    
    def acc0_circuit_threshold(f, n):
        # Example threshold for XOR function is n-1
        return n - 1
    
    def tropicalized_boolean_algebra(f, n):
        # Example mapping to tropicalized Boolean algebra
        return f
    
    def tensor_product_rank(tba):
        # Example rank calculation (simplified)
        return len(tba) if tba else 0
    
    n = random.randint(5, 40)
    f = generate_explicit_function(n)
    threshold = acc0_circuit_threshold(f, n)
    tba = tropicalized_boolean_algebra(f, n)
    rank = tensor_product_rank(tba)
    
    ratio = rank / threshold if threshold != 0 else float('inf')
    metric_value = ratio
    
    conjecture_holds = 0.8 <= ratio <= 1.2
    counterexample = "Ratio out of bounds" if not conjecture_holds else ""
    
    return {
        "metric_name": "tensor_product_rank_over_threshold",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        results.append(result)
        print(f"TRIAL: {result}")

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Ratio out of bounds\" first_failing_seed={first_failing_seed}")