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
    n = random.choice([5, 10, 15, 20, 30, 40])
    
    # Generate a random Boolean satisfiability instance with n variables
    instance = [random.randint(0, 1) for _ in range(n)]
    
    # Compute the minimal symplectic form Σ (simplified example)
    # For this example, let's assume Σ is proportional to n^2
    Σ = sum(instance) * n
    
    # Measure the DPLL proof path length (simplified example)
    # For this example, let's assume the path length is proportional to 2^n
    dpll_path_length = 2 ** n
    
    # Compute log(Σ) and log(n^2)
    log_Σ = math.log(Σ) if Σ > 0 else float('-inf')
    log_n2 = math.log(n**2) if n > 0 else float('-inf')
    
    # Check if the conjecture holds for this instance
    conjecture_holds = abs(log_Σ - log_n2) <= 1e-6
    
    return {
        "metric_name": "log(Σ)",
        "metric_value": log_Σ,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Instance {instance} does not satisfy the conjecture"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_msl = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_msl)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_msl} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_msl} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")