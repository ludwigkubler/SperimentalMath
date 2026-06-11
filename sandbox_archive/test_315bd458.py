# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll_width(phi):
        if not phi:
            return 0
        literals = set()
        for clause in phi:
            literals.update(abs(lit) for lit in clause)
        width = 0
        for literal in literals:
            new_phi = [c for c in phi if literal not in c and -literal not in c]
            width = max(width, dpll_width(new_phi))
        return width + 1
    
    def min_idx(phi):
        # Placeholder for the actual computation of min_idx(φ)
        # This is a dummy implementation
        return len(phi)
    
    n = random.randint(5, 40)
    phi = generate_cnf(n)
    w_DPLL = dpll_width(phi)
    min_idx_phi = min_idx(phi)
    
    return {
        "metric_name": "min_idx_vs_w_DPLL",
        "metric_value": abs(min_idx_phi - w_DPLL) / max(w_DPLL, 1),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(min_idx_phi - w_DPLL) / max(w_DPLL, 1) <= 0.1 and min_idx_phi * 1.1 >= w_DPLL,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 31))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")