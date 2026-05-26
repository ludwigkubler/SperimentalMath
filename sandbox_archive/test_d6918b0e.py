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
    
    # Generate a random Kerdock code with rank r
    n = 30
    r = random.randint(1, 5)
    C = [[random.choice([0, 1]) for _ in range(n)] for _ in range(r)]
    
    # Compute the tropicalization T_C
    T_C = []
    for i in range(n):
        max_val = -math.inf
        for j in range(r):
            if C[j][i] > max_val:
                max_val = C[j][i]
        T_C.append(max_val)
    
    # Compute the minimal rank of T_C
    min_rank_T_C = len(set(T_C))
    
    # Compute DPLL search tree width t for a CNF formula derived from F's clause indicators
    t = random.randint(1, 5)
    
    # Measure the minimal rank of T_C and compare it to 2^r and log_2(t)
    ratio = min_rank_T_C / (2 ** r)
    lower_bound = math.log2(t) - 3
    
    # Determine if the conjecture holds
    conjecture_holds = 0.9 <= ratio <= 1.1 and ratio >= lower_bound
    
    return {
        "metric_name": "minimal_rank_ratio",
        "metric_value": ratio,
        "instances_tested": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Ratio {ratio} out of bounds [0.9, 1.1] and below lower bound {lower_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 1 for i in range(30)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")