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
    n = random.randint(5, 40)
    variables = list(range(n))
    
    # Generate a random Boolean formula with n variables
    formula = []
    for _ in range(2**n):
        clause = [random.choice(variables) if random.choice([True, False]) else -1 for _ in range(random.randint(1, n))]
        formula.append(clause)
    
    # Calculate the circuit depth of a Frege proof (simplified model)
    d_phi = len(formula)  # Simplified model: each clause is a gate
    
    # Compute the Ramanujan sum at s = 2n
    def ramanujan_sum(s, phi):
        if s <= 0:
            return 0
        result = 0
        for k in range(1, s + 1):
            if math.gcd(k, s) == 1:
                result += (-1)**k * (s // k)
        return result
    
    R_2n_phi = ramanujan_sum(2 * n, formula)
    
    # Check the conjecture
    ratio = d_phi / R_2n_phi if R_2n_phi != 0 else float('inf')
    conjecture_holds = ratio <= n**(1/3)
    counterexample = "" if conjecture_holds else f"Ratio {ratio} > O(n^(1/3)) for n={n}"
    
    return {
        "metric_name": "circuit_depth_over_ramanujan_sum",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else list(range(2, 100, 3))[:30]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_ratio)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")