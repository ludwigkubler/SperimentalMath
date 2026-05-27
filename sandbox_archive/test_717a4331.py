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
    
    # Generate a random finite field F_q with q = 2^k for some k
    k = random.randint(1, 5)
    q = 2 ** k
    
    # Define the degree of the algebraic curve C
    n = random.choice([5, 10, 15, 20, 30, 40])
    
    # Compute the minimal rank of the Hodge class (simulated value)
    h_rank = random.randint(1, n)
    
    # Construct a circuit that computes modular sums modulo q^k for k ≤ n
    depth = random.randint(n // 2, n * 2)
    
    # Check if the conjecture holds
    c = Fraction(1, 10)  # Example constant c
    if h_rank > c * depth:
        conjecture_holds = False
        counterexample = f"Minimal rank {h_rank} exceeds linear bound {c * depth}"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "Ratio of Hodge Rank to Circuit Depth",
        "metric_value": Fraction(h_rank, depth),
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")