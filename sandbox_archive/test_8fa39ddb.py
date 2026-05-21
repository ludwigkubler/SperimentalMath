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
    
    def generate_matroid(n):
        matroid = set()
        for i in range(n):
            matroid.add(frozenset(random.sample(range(1, n+1), i+1)))
        return matroid
    
    def min_distance(matroid):
        distances = {}
        for m1 in matroid:
            for m2 in matroid:
                if m1 != m2:
                    distance = sum(1 for x in m1 if x not in m2)
                    distances[(m1, m2)] = distance
                    distances[(m2, m1)] = distance
        return min(distances.values())
    
    def monotone_circuit_size(n):
        # This is a placeholder function. Implement the actual circuit size calculation.
        return 2**n
    
    n = random.randint(5, 40)
    matroid = generate_matroid(n)
    min_dist = min_distance(matroid)
    circuit_size = monotone_circuit_size(n)
    
    if circuit_size == 0:
        return {
            "metric_name": "Ratio of min distance to circuit size",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Circuit size is zero"
        }
    
    ratio = min_dist / circuit_size
    conjecture_holds = ratio >= (2**(n/4) / math.log(n))
    counterexample = f"Ratio {ratio} < Ω(2^{n/4}/log({n})) for n={n}" if not conjecture_holds else ""
    
    return {
        "metric_name": "Ratio of min distance to circuit size",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")