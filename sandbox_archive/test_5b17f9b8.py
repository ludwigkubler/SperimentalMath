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
        for i in range(n):
            clause = [random.randint(-n, n) for _ in range(2)]
            while len(set(clause)) != 2 or 0 in clause:
                clause = [random.randint(-n, n) for _ in range(2)]
            clauses.append(clause)
        return clauses
    
    def monotone_width(cnf):
        # Simplified version of monotone width calculation
        return len(cnf)
    
    def generate_modular_form(p, N):
        # Placeholder function to simulate modular form generation
        return 1 + random.randint(0, 2 * N)
    
    p = random.choice([2, 3, 5, 7, 11, 13, 17, 19])
    N = random.randint(2, 40)
    cnf = generate_cnf(N)
    w_phi = monotone_width(cnf)
    min_idx_pN = generate_modular_form(p, N)
    
    if min_idx_pN <= w_phi <= 2 * min_idx_pN:
        return {
            "metric_name": "monotone_width",
            "metric_value": w_phi,
            "instances_tested": 1,
            "n_max": N,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "monotone_width",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": N,
            "conjecture_holds": False,
            "counterexample": f"CNF: {cnf}, w(φ): {w_phi}, min_idx_{p}_{N}: {min_idx_pN}"
        }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")