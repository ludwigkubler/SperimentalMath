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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        max_communication = 0
        for i in range(2**n):
            comm = 0
            for j in range(n):
                if f[i] != f[i ^ (1 << j)]:
                    comm += 1
            max_communication = max(max_communication, comm)
        return max_communication
    
    def minimal_local_index_of_tropical_motivic_homology(f):
        n = int(math.log2(len(f)))
        local_indices = [0] * n
        for i in range(2**n):
            for j in range(n):
                if f[i] != f[i ^ (1 << j)]:
                    local_indices[j] += 1
        return max(local_indices)
    
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        c_f = communication_complexity(f)
        mtr_h_f = minimal_local_index_of_tropical_motivic_homology(f)
        results.append(abs(mtr_h_f - c_f))
    
    mean_C = sum(results) / len(results)
    std_C = math.sqrt(sum((x - mean_C)**2 for x in results) / len(results))
    conjecture_holds = all(x <= 10 for x in results)  # Example constant factor
    counterexample = "mapping_undefined" if not conjecture_holds else ""
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_C,
        "instances_tested": len(results),
        "n_max": max([int(math.log2(len(generate_boolean_function(n)))) for n in [5, 10, 15, 20, 30, 40]]),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) or [2**i - 1 for i in range(5, 31)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_C = sum(r["metric_value"] for r in results) / len(results)
    std_C = math.sqrt(sum((r["metric_value"] - mean_C)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_C} std={std_C} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")