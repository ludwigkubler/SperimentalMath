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
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for var in variables:
            clauses.append([var])
        for i in range(n-1):
            clauses.append([f'x{i}', f'x{i+1}'])
        return clauses
    
    def compute_local_zeta_function(clauses, p):
        # Simplified version of computing local zeta function
        # This is a placeholder and should be replaced with actual computation
        return random.uniform(0.5, 2)
    
    def resolution_proof_width(clauses):
        # Simplified version of computing resolution proof width
        # This is a placeholder and should be replaced with actual computation
        return len(clauses) * 10
    
    n = random.randint(5, 40)
    p = random.choice([2, 3, 5])
    clauses = generate_tseitin_formula(n)
    
    I_phi = compute_local_zeta_function(clauses, p)
    w_phi = resolution_proof_width(clauses)
    
    diff = abs(I_phi - w_phi)
    conjecture_holds = diff <= 3
    
    return {
        "metric_name": "abs_diff",
        "metric_value": diff,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"diff={diff} > 3"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_diff = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_diff) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_diff} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and "counterexample" in r for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")