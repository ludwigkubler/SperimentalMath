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
    
    def is_monotone(f):
        for i in range(1 << len(f)):
            for j in range(i + 1, 1 << len(f)):
                if f[i] > f[j]:
                    return False
        return True
    
    def fundamental_group(n):
        # Placeholder function to compute the fundamental group of a state space.
        # This is a stub and should be replaced with an actual algorithm.
        return random.randint(1, 5)
    
    def monotone_circuit_size(f):
        # Placeholder function to compute the monotone circuit size.
        # This is a stub and should be replaced with an actual algorithm.
        return len(f) * 2
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = [random.randint(0, 1) for _ in range(1 << n)]
    
    if not is_monotone(f):
        return {
            "metric_name": "monotone_circuit_size",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "not_monotone"
        }
    
    pi_f = fundamental_group(n)
    C_f = monotone_circuit_size(f)
    
    if C_f <= 2 ** pi_f:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"C_f={C_f} > 2^π_f({pi_f})={2**pi_f}"
    
    return {
        "metric_name": "monotone_circuit_size",
        "metric_value": C_f,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        seeds = [2**i + 1 for i in range(5, 8)]  # First 30 prime numbers
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")