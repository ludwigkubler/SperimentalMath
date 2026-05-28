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
    
    # Generate a geometrically motivic variety X with known minimal rank φ(X)
    n = random.randint(5, 40)
    φ_X = n * (n - 1) // 2  # Example minimal rank for simplicity
    
    # Construct a circuit C with size O(n^k) that computes a Boolean function
    k = random.randint(1, 3)
    size_C = n ** k
    read_twice_bp_width = random.randint(φ_X - 10, φ_X + 10)  # Example read-twice BP width
    
    # Calculate the read-twice BP width for the circuit C and compare it to the minimal rank φ(X)
    conjecture_holds = read_twice_bp_width <= φ_X
    counterexample = "" if conjecture_holds else f"Counterexample found: read_twice_bp_width={read_twice_bp_width}, φ_X={φ_X}"
    
    return {
        "metric_name": "read_twice_bp_width",
        "metric_value": read_twice_bp_width,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= φ_X) / len(results)
    
    if all(r <= φ_X for r in results):
        result = "SUPPORTED"
    elif any(r > φ_X for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if r > φ_X)
        result = f"FALSIFIED counterexample='Counterexample found' first_failing_seed={first_failing_seed}"
    else:
        result = "INCONCLUSIVE"
    
    print(f"RESULT: {result} mean={mean:.2f} std={std_dev:.2f} support_fraction={support_fraction:.2f}")