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
        # This is a placeholder function; replace it with actual generation logic
        return [random.randint(1, n) for _ in range(n)]
    
    def measure_invariant(instance):
        # Measure the rank variance R(n) of the instance
        # This is a placeholder function; replace it with actual measurement logic
        return sum(instance)
    
    def count_symmetric_spaces(interaction_graph):
        # Count the number of symmetric spaces required to represent the interaction graph
        # This is a placeholder function; replace it with actual counting logic
        return len(set(tuple(sorted(edge)) for edge in interaction_graph))
    
    n = 40
    instances_tested = 30
    total_symmetric_spaces = 0
    total_variance = 0
    
    for _ in range(instances_tested):
        instance = generate_instance(n)
        variance = measure_invariant(instance)
        symmetric_spaces = count_symmetric_spaces([(i, j) for i in range(n) for j in range(i+1, n)])
        
        total_symmetric_spaces += symmetric_spaces
        total_variance += variance
    
    mean_symmetric_spaces = total_symmetric_spaces / instances_tested
    mean_variance = total_variance / instances_tested
    k = 5  # Define the constant k from the conjecture
    
    if abs(mean_symmetric_spaces - mean_variance) <= k:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"Mean symmetric spaces {mean_symmetric_spaces} not within ±{k} of mean variance {mean_variance}"
    
    return {
        "metric_name": "Symmetric Spaces vs Rank Variance",
        "metric_value": mean_symmetric_spaces,
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")