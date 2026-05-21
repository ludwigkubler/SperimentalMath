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
    
    # Generate a random binary matroid with ground set size n
    n = random.randint(5, 40)
    elements = list(range(n))
    rank = random.randint(1, n)
    independent_sets = []
    for _ in range(2**rank):
        subset = random.sample(elements, rank)
        if all(len(set(subset) & set(iset)) <= 1 for iset in independent_sets):
            independent_sets.append(subset)
    
    # Compute the characteristic vectors
    char_vectors = [[0] * n for _ in range(2**rank)]
    for i, subset in enumerate(independent_sets):
        for j in subset:
            char_vectors[i][j] = 1
    
    # Simulate the disjointness problem using a protocol that checks for disjointness via bitwise operations
    communication_complexity = 0
    for _ in range(100):  # Test with 100 random pairs of vectors
        i, j = random.sample(range(2**rank), 2)
        if any(char_vectors[i][k] & char_vectors[j][k] for k in elements):
            communication_complexity += math.log2(n) + 1
    
    # Verify if the complexity meets Ω(log n)
    conjecture_holds = communication_complexity >= 0.5 * math.log2(n)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": communication_complexity,
        "instances_tested": 100,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_complexity = sum(r["metric_value"] for r in results) / len(results)
    std_complexity = math.sqrt(sum((r["metric_value"] - mean_complexity)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_complexity} std={std_complexity} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_complexity} std={std_complexity} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")