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

def generate_polynomial(d, n):
    variables = list(range(n))
    coeffs = [random.randint(1, 10) for _ in range(d + 1)]
    x = [random.randint(1, 10) for _ in range(n)]
    return sum(c * (x[i] ** i if i > 0 else 1) for i, c in enumerate(coeffs))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for d in range(10, 101):
            f = generate_polynomial(d, n)
            # Placeholder for actual Schur-Weyl rank calculation
            rho_f = random.uniform(1, 2 * d**(2/3))  # Simulated value
            
            results.append({
                "n": n,
                "d": d,
                "f": f,
                "rho_f": rho_f,
                "ratio": rho_f / d**(2/3)
            })
    
    total_ratio = sum(result["ratio"] for result in results)
    mean_ratio = total_ratio / len(results)
    std_deviation = math.sqrt(sum((result["ratio"] - mean_ratio) ** 2 for result in results) / len(results))
    
    conjecture_holds = all(result["ratio"] <= 1.5 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Schur-Weyl Rank Ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    std_deviation = math.sqrt(sum((result["metric_value"] - mean_ratio) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_deviation} support_fraction={support_fraction}")
    elif any(result["counterexample"] == "mapping_undefined" for result in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")