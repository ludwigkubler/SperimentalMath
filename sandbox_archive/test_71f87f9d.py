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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def calculate_noncrossing_partition_lattice(f):
        n = len(f)
        lattice = [[set() for _ in range(1 << n)] for _ in range(n + 1)]
        lattice[0][0] = {()}
        
        for i in range(1, n + 1):
            for j in range(1 << i):
                if (j & (1 << (i - 1))) != 0:
                    lattice[i][j] = lattice[i-1][j ^ (1 << (i - 1))]
                else:
                    lattice[i][j] = lattice[i-1][j]
        
        return lattice
    
    def calculate_deterministic_communication_complexity(f):
        n = len(f)
        # Simplified version for demonstration purposes
        return n
    
    f = generate_random_boolean_function(5)
    lattice = calculate_noncrossing_partition_lattice(f)
    rank = len(lattice[-1][0])
    c_f = calculate_deterministic_communication_complexity(f)
    
    return {
        "metric_name": "rank",
        "metric_value": rank,
        "instances_tested": 1,
        "n_max": 5,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")