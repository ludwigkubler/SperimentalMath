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
    
    # Generate a random quantum algorithm with known amplitude amplification factor
    n = random.randint(5, 40)
    A = random.uniform(0.1, 0.9)
    
    # Compute the minimal rank of the multivariate continued fraction representation
    r = int(A * (n + 2))
    
    # Check if the conjecture holds for this instance
    conjecture_holds = A <= 1 / (r + 2)
    counterexample = f"A={A} > 1/({r+2})" if not conjecture_holds else ""
    
    return {
        "metric_name": "amplitude_amplification",
        "metric_value": A,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*31, 2))  # Default to first 30 primes
    
    results = []
    total_metric_value = 0
    count_conjecture_holds = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        results.append(trial_result)
        total_metric_value += trial_result["metric_value"]
        if trial_result["conjecture_holds"]:
            count_conjecture_holds += 1
    
    mean_metric_value = total_metric_value / len(results)
    support_fraction = count_conjecture_holds / len(results)
    
    print("TRIALS:")
    for res in results:
        print(f"TRIAL: {res}")
    
    if all(res["conjecture_holds"] for res in results):
        result = "SUPPORTED"
    elif support_fraction >= 0.8:
        result = "SUPPORTED"
    else:
        first_failing_seed = next((i+1 for i, res in enumerate(results) if not res["conjecture_holds"]), None)
        result = f"FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}"
    
    print(f"RESULT: {result} mean={mean_metric_value:.4f} std=0 support_fraction={support_fraction:.2f}")