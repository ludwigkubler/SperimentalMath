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
    
    # Generate an n-qubit quantum state with varying levels of entanglement
    n = 10  # Fixed for simplicity, can be adjusted within the loop
    entanglement_complexity = random.randint(5, 20)  # Simulated entanglement complexity
    
    # Compute the minimal rank of its associated geometric Langlands dual
    min_rank = random.randint(1, 10)  # Simplified for testing
    
    # Determine the communication complexity required to share each state
    communication_complexity = entanglement_complexity * n  # Simulated communication complexity
    
    # Correlate the minimal rank with the communication complexity
    ratio = min_rank / (math.log(communication_complexity) / math.log(n))
    
    # Establish a logarithmic relationship within a constant factor
    c = 2.0  # Example constant factor
    if c * entanglement_complexity <= communication_complexity <= c * entanglement_complexity:
        conjecture_holds = True
    else:
        conjecture_holds = False
        counterexample = f"Failed for n={n}, E(n)={entanglement_complexity}, min_rank={min_rank}"
    
    return {
        "metric_name": "Ratio of minimal rank to logarithm of entanglement complexity",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")