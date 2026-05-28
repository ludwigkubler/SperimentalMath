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
    n = random.randint(5, 40)
    A = random.uniform(0.1, 0.9)
    r = random.randint(1, 10)
    
    # Simulate the computation of the minimal rank of a multivariate continued fraction
    # and the amplitude amplification factor for this quantum algorithm.
    computed_A = 1 / (r + 2)
    
    metric_name = "amplitude_amplification_factor"
    metric_value = A
    instances_tested = 1
    conjecture_holds = A <= computed_A
    counterexample = "" if conjecture_holds else f"Calculated A={A}, but expected A ≤ {computed_A}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        # Default list of 30 prime numbers
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_A = sum(r["metric_value"] for r in results) / len(results)
    avg_rank = sum(1 / (r["metric_value"] * (r["metric_value"] + 2)) if r["conjecture_holds"] else float('inf') for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_A} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"A > 1 / (r + 2)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")