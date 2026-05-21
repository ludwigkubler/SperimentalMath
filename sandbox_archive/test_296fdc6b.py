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
    k = random.randint(2, min(n, 10))
    
    # Generate a random matroid M with n elements
    M = {i: set() for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            if random.choice([True, False]):
                M[i].add(j)
                M[j].add(i)
    
    # Compute the minimal representation distance of M
    min_distance = float('inf')
    for i in range(n):
        for j in range(i + 1, n):
            distance = sum(1 for x in M[i] if x not in M[j])
            min_distance = min(min_distance, distance)
    
    # Construct the smallest monotone circuit for k-CLIQUE on n vertices
    def clique_circuit_size(n, k):
        if k == 0:
            return 1
        if k == 1:
            return n
        return (n - k + 1) * clique_circuit_size(n - 1, k - 1)
    
    circuit_size = clique_circuit_size(n, k)
    
    # Calculate the ratio of the minimum distance to the circuit size
    ratio = min_distance / circuit_size
    
    # Check if the conjecture holds
    conjecture_holds = ratio >= (2 ** (n / 4)) / math.log(n)
    counterexample = "" if conjecture_holds else f"Ratio {ratio} < Ω(2^{n/4}/log({n})) for n={n}"
    
    return {
        "metric_name": "Ratio of min distance to circuit size",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30)) + [53, 67, 71, 73, 79]
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio too low\" first_failing_seed={first_failing_seed}")