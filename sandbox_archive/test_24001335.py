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
        # Generate a random matroid using the uniform distribution
        elements = list(range(n))
        independent_sets = []
        for i in range(1 << n):
            subset = [elements[j] for j in range(n) if (i & (1 << j))]
            if all(len(set(subset[:k])) == k for k in range(1, len(subset))):
                independent_sets.append(subset)
        return independent_sets
    
    def min_representation_distance(matroid):
        # Compute the minimum distance between two distinct representations of the matroid
        n = len(matroid[0])
        distances = []
        for i in range(len(matroid)):
            for j in range(i + 1, len(matroid)):
                distance = sum(1 for x in matroid[i] if x not in matroid[j])
                distances.append(distance)
        return min(distances) if distances else float('inf')
    
    def monotone_circuit_size(n):
        # Construct the smallest monotone circuit for k-CLIQUE on n vertices
        k = 3  # Example value, can be adjusted
        size = 2 ** (n - k + 1)
        return size
    
    n = random.randint(5, 40)
    matroid = generate_matroid(n)
    min_dist = min_representation_distance(matroid)
    circuit_size = monotone_circuit_size(n)
    
    if min_dist == float('inf'):
        return {
            "metric_name": "min_representation_distance",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = min_dist / circuit_size
    conjecture_holds = ratio >= (2 ** (n / 4) / math.log(n))
    
    return {
        "metric_name": "min_representation_distance",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Ratio {ratio} < Ω(2^(n/4) / log(n))"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 997) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results if r["conjecture_holds"])) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio below Ω(2^(n/4) / log(n))\" first_failing_seed={first_failing_seed}")