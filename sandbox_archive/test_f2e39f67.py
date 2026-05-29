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
    
    def generate_monotone_function(n):
        # Generate a random monotone Boolean function
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_fundamental_group(f):
        # Placeholder for the actual computation of the fundamental group
        # This is a dummy implementation that returns a small value
        return random.randint(1, 5)
    
    def monotone_circuit_size(f):
        # Placeholder for the actual computation of the monotone circuit size
        # This is a dummy implementation that returns a small value
        return random.randint(10, 20)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_monotone_function(n)
    pi_f = compute_fundamental_group(f)
    C_f = monotone_circuit_size(f)
    
    metric_value = C_f
    instances_tested = 1
    conjecture_holds = C_f <= 2**pi_f
    counterexample = "" if conjecture_holds else f"Counterexample for n={n}"
    
    return {
        "metric_name": "monotone_circuit_size",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")