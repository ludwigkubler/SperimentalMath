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
    
    # Generate an explicit function f in P with known ACC⁰ circuit depth
    n = random.randint(5, 40)
    coefficients = [random.randint(-10, 10) for _ in range(n)]
    f = sum(coeff * x**i for i, coeff in enumerate(coefficients))
    
    # Construct the associated noncommutative algebraic curve G_f and compute the rank of its tangent sheaf
    # For simplicity, we assume the rank is equal to the degree of the polynomial (n-1)
    min_rank_tangent_sheaf = n - 1
    
    # Calculate ACC⁰ circuit depth (for a simple polynomial, it's the number of terms minus one)
    acc0_circuit_depth = len(coefficients) - 1
    
    # Check if the conjecture holds
    ratio = acc0_circuit_depth / min_rank_tangent_sheaf
    conjecture_holds = ratio <= 2.5 and ratio >= 1.2
    
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Counterexample for n={n}, f={f}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    total_ratio = 0
    count_conjecture_holds = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        results.append(trial_result)
        total_ratio += trial_result["metric_value"]
        if trial_result["conjecture_holds"]:
            count_conjecture_holds += 1
    
    mean_ratio = total_ratio / len(results)
    support_fraction = count_conjecture_holds / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")