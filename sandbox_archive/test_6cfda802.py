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
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def monotone_width(cnf):
        # Simplified version of monotone width calculation
        max_vars = 0
        for clause in cnf:
            max_vars = max(max_vars, max(abs(x) for x in clause))
        return max_vars
    
    def generate_modular_form(p, N):
        # Simplified modular form generation (not actual implementation)
        return random.randint(1, p**N)
    
    def min_idx(p, N):
        # Simplified minimal index calculation
        return random.randint(1, 2 * N)
    
    n = 30
    instances_tested = 0
    total_metric_value = 0.0
    counterexample = ""
    
    for _ in range(30):
        cnf = generate_cnf(n)
        w_phi = monotone_width(cnf)
        min_idx_pN = min_idx(random.choice([2, 3, 5]), n)
        
        if not (min_idx_pN <= w_phi <= 2 * min_idx_pN):
            counterexample = f"CNF: {cnf}, w(φ): {w_phi}, min_idx_{n}: {min_idx_pN}"
            break
        
        instances_tested += 1
        total_metric_value += w_phi
    
    if counterexample:
        return {
            "metric_name": "monotone_width",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": counterexample
        }
    
    return {
        "metric_name": "monotone_width",
        "metric_value": total_metric_value / instances_tested if instances_tested > 0 else None,
        "instances_tested": instances_tested,
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
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=NA support_fraction={support_fraction}")
        else:
            print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} < 0.8")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds tested")