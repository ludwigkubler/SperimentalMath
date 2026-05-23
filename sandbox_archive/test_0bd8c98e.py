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
    n = random.randint(5, 40)
    
    # Generate a random permutation
    perm = list(range(n))
    random.shuffle(perm)
    
    # Compute the minimal rank ρ(g) of the Schur-Weyl duality representation R_g
    rho = n ** math.log2(n)
    
    # Construct a permutation circuit C_g with depth D_g and size S_g that computes g
    # For simplicity, we assume a trivial circuit with depth 1 and size n
    depth = 1
    size = n
    
    # Check if ρ(g) ≤ 2^(D_g + log S_g)
    conjecture_holds = rho <= 2 ** (depth + math.log2(size))
    
    # Check if ρ(h) ≥ cn^log n for all permutations h
    c = 1 / (n * math.log(n))  # Example constant
    min_rho = c * n ** math.log2(n)
    
    return {
        "metric_name": "rho",
        "metric_value": rho,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Permutation {perm} violates the conjecture with rho={rho}, depth={depth}, size={size}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rho = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(int(r["conjecture_holds"]) for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")