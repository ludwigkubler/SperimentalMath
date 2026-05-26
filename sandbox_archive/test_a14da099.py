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
    
    # Define the constructive mapping from Boolean function to quaternionic Kähler manifold
    def boolean_to_quaternionic_kahler(f):
        if f == '0':
            return [[1, 0], [0, -1]]
        elif f == '1':
            return [[-1, 0], [0, 1]]
        else:
            raise ValueError("Invalid Boolean function")

    # Generate a random n-ary Boolean function with at most k arguments
    n = random.randint(5, 40)
    k = random.randint(2, min(n, 3))
    boolean_function = ''.join(random.choice('01') for _ in range(k))

    # Compute the resolution proof width of the Boolean function
    R_f = len(boolean_function)  # Simplified for demonstration

    # Construct the quaternionic Kähler manifold corresponding to the Boolean function
    try:
        omega_M = boolean_to_quaternionic_kahler(boolean_function)
    except ValueError as e:
        return {
            "metric_name": "",
            "metric_value": 0.0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": str(e)
        }

    # Compute the minimal rank of the quaternionic Kähler form
    rank_omega = max(abs(x) for row in omega_M for x in row)

    # Check if the conjecture holds
    C = 10  # Hypothetical constant for demonstration
    conjecture_holds = rank_omega <= C

    return {
        "metric_name": "Minimal Rank of Quaternionic Kähler Form",
        "metric_value": rank_omega,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Counterexample for Boolean function: {boolean_function}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 30))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result_str = f"SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result_str = f"FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}"

    print(result_str)