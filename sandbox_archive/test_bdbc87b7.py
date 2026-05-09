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

def generate_random_vector(n):
    return [random.random() for _ in range(n)]

def dot_product(v1, v2):
    return sum(x * y for x, y in zip(v1, v2))

def vector_add(v1, v2):
    return [x + y for x, y in zip(v1, v2)]

def vector_subtract(v1, v2):
    return [x - y for x, y in zip(v1, v2)]

def norm(v):
    return sum(x**2 for x in v)**0.5

def monte_carlo_volume(n, samples=100000):
    count = 0
    for _ in range(samples):
        point = generate_random_vector(n)
        if all(point[i] + random.random() <= 1 for i in range(n)):
            count += 1
    return (count / samples) * n**n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    volume = monte_carlo_volume(n)
    communication_complexity = n
    
    metric_name = "communication_complexity"
    metric_value = communication_complexity
    instances_tested = 1
    conjecture_holds = communication_complexity >= math.log(volume)
    counterexample = "" if conjecture_holds else f"Volume={volume}, CC={communication_complexity}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 1 for i in range(5, 6)]  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Volume too small\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")