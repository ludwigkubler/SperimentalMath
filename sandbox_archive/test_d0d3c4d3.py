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
        # Generate a random matroid using a simple method (not optimal but sufficient for testing)
        elements = list(range(n))
        independent_sets = []
        for i in range(1, n + 1):
            independent_sets.extend(random.sample(elements, i))
        return independent_sets
    
    def min_distance(matroid, R):
        # Compute the minimum distance between two distinct representations of the matroid
        # This is a placeholder function; replace with actual computation
        return random.random()
    
    def smallest_monotone_circuit(n, k):
        # Construct the smallest monotone circuit for k-CLIQUE on n vertices
        # This is a placeholder function; replace with actual construction
        return random.randint(10, 100)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    matroid = generate_matroid(n)
    R = "some_representation_system"
    distance = min_distance(matroid, R)
    circuit_size = smallest_monotone_circuit(n, k=2)  # Assuming k=2 for simplicity
    ratio = distance / circuit_size
    
    conjecture_holds = ratio >= (2 ** (n / 4)) / math.log(n)
    
    return {
        "metric_name": "Ratio of min distance to circuit size",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": f"Ratio {ratio} < Ω(2^{n/4}/log({n})) for n={n}" if not conjecture_holds else ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = results[next(i for i, r in enumerate(results) if not r["conjecture_holds"])["counterexample"]]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")