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
    
    def generate_instance(n):
        # Generate a random communication complexity instance with rank variance R(n)
        return [random.randint(1, n) for _ in range(n)]
    
    def measure_invariant(instance):
        # Construct the interaction graph and determine the number of symmetric spaces required
        n = len(instance)
        symmetric_spaces = set()
        
        for i in range(n):
            for j in range(i + 1, n):
                if instance[i] == instance[j]:
                    symmetric_spaces.add((i, j))
        
        return len(symmetric_spaces)
    
    def rank_variance(instance):
        # Calculate the rank variance R(n) of the instance
        n = len(instance)
        mean = sum(instance) / n
        variance = sum((x - mean) ** 2 for x in instance) / n
        return variance
    
    instances_tested = 0
    total_symmetric_spaces = 0
    total_variance = 0
    n_max = 1
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            instance = generate_instance(n)
            symmetric_spaces = measure_invariant(instance)
            variance = rank_variance(instance)
            
            total_symmetric_spaces += symmetric_spaces
            total_variance += variance
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_symmetric_spaces = total_symmetric_spaces / instances_tested
    mean_variance = total_variance / instances_tested
    
    k = 5  # Define the constant k for the conjecture
    conjecture_holds = abs(mean_symmetric_spaces - mean_variance) <= k
    counterexample = "" if conjecture_holds else f"Mean symmetric spaces {mean_symmetric_spaces} not within ±{k} of mean variance {mean_variance}"
    
    return {
        "metric_name": "Symmetric Spaces vs Rank Variance",
        "metric_value": mean_symmetric_spaces,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")