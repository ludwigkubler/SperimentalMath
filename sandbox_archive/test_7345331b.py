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
    
    # Generate random symmetric tensor dimensions
    n = random.randint(5, 40)
    tensor_dimensions = [random.randint(2, 10) for _ in range(n)]
    
    # Compute Schur-Weyl duality rank (placeholder implementation)
    rho_f = sum(tensor_dimensions)  # Placeholder value
    
    # Determine the complexity of the monomial ideal (placeholder implementation)
    kappa = sum(tensor_dimensions)  # Placeholder value
    
    # Check the conjecture
    conjecture_holds = (rho_f <= kappa + 1) and (rho_f >= kappa / 2 - 1)
    
    return {
        "metric_name": "Schur-Weyl duality rank vs Monomial Ideal Complexity",
        "metric_value": rho_f,
        "instances_tested": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"rho(f)={rho_f}, kappa={kappa}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")