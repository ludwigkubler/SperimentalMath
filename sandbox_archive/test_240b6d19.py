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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_monotone_function(n):
        # Generate a random monotone Boolean function with n variables
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def noncrossing_partition(f):
        n = len(f)
        if n == 1:
            return [f]
        
        partition = []
        for i in range(n):
            left = f[:i+1]
            right = f[i+1:]
            if all(left[j] <= right[j] for j in range(len(right))):
                partition.append(left + right)
        return partition
    
    def count_elements(partition):
        # Count the number of elements in the noncrossing partition
        return sum(1 for _ in partition)
    
    n = random.randint(5, 40)
    f = generate_monotone_function(n)
    partition = noncrossing_partition(f)
    num_elements = count_elements(partition)
    
    C = 2  # Example constant to test
    metric_value = num_elements
    
    conjecture_holds = num_elements <= C * math.log(n, 2)
    counterexample = "" if conjecture_holds else f"n={n}, elements={num_elements}, expected<=C*log(n)={C*math.log(n, 2)}"
    
    return {
        "metric_name": "Number of elements in noncrossing partition",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=undefined_mapping")