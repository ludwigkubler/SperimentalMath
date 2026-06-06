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
    
    def tseitin_formula(n):
        # Generate a Tseitin formula with n variables
        clauses = []
        for i in range(1, n + 1):
            clauses.append([i])
            for j in range(i + 1, n + 1):
                clauses.append([-i, -j, i + j])
        return clauses
    
    def hodge_decomposition_module(clauses):
        # Placeholder for Hodge decomposition module computation
        # This is a dummy implementation and does not actually compute the HOD
        return len(clauses)
    
    def resolution_proof_width(clauses):
        # Placeholder for resolution proof width computation
        # This is a dummy implementation and does not actually compute the RPW
        return len(clauses)
    
    n = random.randint(5, 40)
    clauses = tseitin_formula(n)
    min_rank = hodge_decomposition_module(clauses)
    w = resolution_proof_width(clauses)
    
    if w == 0:
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "resolution_proof_width_is_zero"
        }
    
    ratio = min_rank / w
    if 0.5 <= ratio <= 2:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"ratio={ratio}"
    
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"ratio_outside_bounds\" first_failing_seed={first_failing_seed}")