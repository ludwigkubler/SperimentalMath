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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def monotone_width(cnf):
        # Simplified version of monotone width calculation
        return len(cnf)
    
    def generate_modular_form(p, N):
        # Placeholder for modular form generation
        # This is a dummy function and should be replaced with actual implementation
        return random.randint(1, 100)
    
    p = random.choice([2, 3, 5, 7, 11, 13, 17, 19])
    N = random.randint(2, 4)
    cnf = generate_cnf(N)
    w_phi = monotone_width(cnf)
    min_idx_pN = generate_modular_form(p, N)
    
    if w_phi < min_idx_pN or w_phi > 2 * min_idx_pN:
        return {
            "metric_name": "monotone_width",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": N,
            "conjecture_holds": False,
            "counterexample": f"CNF: {cnf}, w(φ): {w_phi}, min_idx_{p}_{N}: {min_idx_pN}"
        }
    
    return {
        "metric_name": "monotone_width",
        "metric_value": w_phi,
        "instances_tested": 1,
        "n_max": N,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r for r in results if not r["conjecture_holds"])["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")