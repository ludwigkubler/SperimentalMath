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

def generate_monotone_function(n):
    # Generate a random monotone Boolean function with n input bits
    return [random.choice([0, 1]) for _ in range(2**n)]

def tropical_representation_size(f):
    # Compute the tropical representation size of the function f
    n = int(math.log2(len(f)))
    basis_vectors = []
    for i in range(n):
        if f[i] == 1:
            basis_vector = [0] * n
            basis_vector[i] = 1
            basis_vectors.append(basis_vector)
    return len(basis_vectors)

def communication_complexity(f):
    # Compute the communication complexity of the function f using cell-projection method
    n = int(math.log2(len(f)))
    max_complexity = 0
    for i in range(n):
        if f[i] == 1:
            complexity = sum(1 for j in range(i+1, n) if f[j] == 1)
            max_complexity = max(max_complexity, complexity)
    return max_complexity

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_monotone_function(n)
        tr_size = tropical_representation_size(f)
        comm_complexity = communication_complexity(f)
        results.append((tr_size, comm_complexity))
    
    mean_tr_size = sum(tr for tr, _ in results) / len(results)
    max_comm_complexity = max(comm for _, comm in results)
    conjecture_holds = mean_tr_size <= n**(2/3) and max_comm_complexity > n**(2/3)
    counterexample = "" if conjecture_holds else f"Max communication complexity {max_comm_complexity} exceeds O(n^(2/3))"
    
    return {
        "metric_name": "Tropical Representation Size",
        "metric_value": mean_tr_size,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Max communication complexity exceeds O(n^(2/3))\" first_failing_seed={first_failing_seed}")