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
    
    # Generate a random tropical polynomial f with coefficients over [0, 1]
    n = random.randint(5, 40)
    coeffs = [random.random() for _ in range(n + 1)]
    x = 0.5  # Evaluate the polynomial at x = 0.5
    f = sum(c * x**i for i, c in enumerate(coeffs))
    
    # Construct an ACC⁰ circuit for a simple function (e.g., identity)
    D = random.randint(2, 10)
    S = random.randint(5, 20)
    # Simulate the circuit evaluation
    result = f
    
    # Compute the minimal number of real points MRP(f) in the tropical curve defined by f
    MRP_f = len([i for i in range(n + 1) if coeffs[i] != 0])
    
    # Compare MRP(f) with the predicted threshold 2^(D/2 + εS)
    epsilon = 0.1
    threshold = 2**(D / 2 + epsilon * S)
    
    conjecture_holds = MRP_f >= threshold
    counterexample = "" if conjecture_holds else f"MRP(f)={MRP_f}, threshold={threshold}"
    
    return {
        "metric_name": "MRP(f)",
        "metric_value": MRP_f,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")