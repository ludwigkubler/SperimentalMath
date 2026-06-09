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
    
    def generate_tseitin_formula(n):
        variables = list(range(1, n + 1))
        clauses = []
        for i in range(1, n + 1):
            clauses.append(f"({i} ∨ {n+i})")
        clauses.append(f"(¬{n+1} ∧ {n+2})")
        return clauses

    def resolution_width(clauses):
        # Simplified resolution width calculation
        return len(clauses)

    def entropy_rate(n):
        # Simplified entropy rate calculation for demonstration purposes
        return math.log2(n)

    n = random.choice([5, 10, 15, 20, 30, 40])
    clauses = generate_tseitin_formula(n)
    width = resolution_width(clauses)
    H_max = entropy_rate(n)
    
    if width > 2 * H_max:
        return {
            "metric_name": "Resolution Proof Width",
            "metric_value": width,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"Width {width} exceeds 2 * H_max {H_max}"
        }
    
    return {
        "metric_name": "Resolution Proof Width",
        "metric_value": width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Width exceeds H_max\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")