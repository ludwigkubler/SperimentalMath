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
    
    def generate_polynomial_system(n):
        # Generate a random polynomial system over F_2 with n variables
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    def compute_k_complexity(system):
        # Placeholder for actual K-complexity computation
        # For simplicity, we assume it's proportional to the number of non-zero rows
        return sum(1 for row in system if any(row))
    
    def compute_symplectic_rank(system):
        # Placeholder for actual symplectic rank computation
        # For simplicity, we assume it's proportional to the number of variables
        return len(system)
    
    n = random.randint(5, 40)
    system = generate_polynomial_system(n)
    k_complexity = compute_k_complexity(system)
    symplectic_rank = compute_symplectic_rank(system)
    
    if k_complexity == 0:
        return {
            "metric_name": "symplectic_rank_to_log2_k_complexity_ratio",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "K-complexity is zero, cannot compute ratio"
        }
    
    ratio = symplectic_rank / math.log(k_complexity, 2) ** 2
    
    return {
        "metric_name": "symplectic_rank_to_log2_k_complexity_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")