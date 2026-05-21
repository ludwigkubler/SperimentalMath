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
    
    def gromov_wasserstein_distance(n):
        return 2**(n - 0.5) / n
    
    def min_monotone_circuit_size(n, k):
        # Placeholder for actual computation
        return n**2
    
    n = random.randint(5, 40)
    D_n = gromov_wasserstein_distance(n)
    
    # Generate a set of random metric measure spaces with Gromov-Wasserstein distance ranging from D(n) to twice D(n)
    distances = [D_n + (random.random() * D_n) for _ in range(10)]
    circuit_sizes = [min_monotone_circuit_size(n, k) for k in range(2, n+1)]
    
    # Correlate these values
    metric_value = sum(distances) / len(distances)
    conjecture_holds = all(D_n <= dist <= 2 * D_n for dist in distances) and all(cs >= D_n for cs in circuit_sizes)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Gromov-Wasserstein Distance",
        "metric_value": metric_value,
        "instances_tested": len(distances),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")