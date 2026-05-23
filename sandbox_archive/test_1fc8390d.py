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
    
    n = 5 + (seed % 4) * 5  # Sweep n through {5,10,15,20,30}
    if n > 40:
        return {
            "metric_name": "communication_complexity",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "n_too_large"
        }
    
    # Generate random binary strings
    strings = [''.join(random.choice('01') for _ in range(n)) for _ in range(30)]
    
    # Compute communication complexity of tensor product
    def tensor_product(s1, s2):
        return ''.join(str(int(a) * int(b)) for a, b in zip(s1, s2))
    
    comm_complexity = 0
    for i in range(len(strings)):
        for j in range(i + 1, len(strings)):
            comm_complexity += len(tensor_product(strings[i], strings[j]))
    
    # Compute minimal rank of configuration space (simplified example)
    def simplicial_complex_rank(n):
        return n * (n - 1) // 2
    
    config_space_rank = sum(simplicial_complex_rank(len(s)) for s in strings)
    
    # Check if the conjecture holds
    if config_space_rank <= comm_complexity:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"config_space_rank={config_space_rank} > comm_complexity={comm_complexity}"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": comm_complexity,
        "instances_tested": 30,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        # Default list of 30 primes
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    # Compute mean and standard deviation
    if all(r["metric_value"] is not None for r in results):
        metric_values = [r["metric_value"] for r in results]
        mean = sum(metric_values) / len(metric_values)
        std_dev = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    else:
        mean, std_dev = None, None
    
    # Compute fraction of seeds where conjecture holds
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='{result['counterexample']}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")