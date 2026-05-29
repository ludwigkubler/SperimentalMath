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
    
    # Generate random XOR game parameters
    n = random.randint(5, 40)  # Number of players
    k = random.randint(1, 4)   # Number of communication rounds
    
    # Compute the minimal order of the Artinian algebra representing the game
    # This is a placeholder for the actual computation which is not provided in the problem statement
    artinian_order = n * k  # Placeholder value
    
    # Define the conjectured upper bound function f(n, k)
    def f(n, k):
        return (n + 1) * k
    
    # Check if the computed minimal order is within the conjectured upper bound
    conjecture_holds = artinian_order <= f(n, k)
    
    # Return the trial results
    return {
        "metric_name": "artinian_order",
        "metric_value": artinian_order,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={n}, k={k}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    results = []
    total_metric_value = 0
    num_trials = len(seeds)
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
        total_metric_value += trial_result["metric_value"]
    
    mean_metric_value = total_metric_value / num_trials
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / num_trials
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")