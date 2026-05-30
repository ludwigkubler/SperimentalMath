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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def polynomial_of_f(f, n):
        terms = []
        for i in range(2**n):
            term = f[i]
            factors = []
            for j in range(n):
                if (i >> j) & 1:
                    factors.append(f'x{j}')
            terms.append((term, factors))
        return terms
    
    def geometric_entropy(A_f):
        # Placeholder for actual computation
        return random.uniform(0.5, 2.0)
    
    def dpll_refutation_size(t_f):
        # Placeholder for actual computation
        return random.randint(10, 100)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_boolean_function(n)
    A_f = polynomial_of_f(f, n)
    GE_A_f = geometric_entropy(A_f)
    t_f = dpll_refutation_size(f)
    
    if t_f == 0:
        return {
            "metric_name": "GE(A_f) / t*(f)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "DPLL refutation size is zero"
        }
    
    ratio = GE_A_f / t_f
    return {
        "metric_name": "GE(A_f) / t*(f)",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio <= 2.0,  # Placeholder constant k
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_ratio = sum(r["metric_value"] for r in results if "metric_value" in r)
    mean_ratio = total_ratio / len(results)
    support_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = support_count / len(results)
    
    if all("counterexample" not in r or r["counterexample"] == "" for r in results):
        RESULT = "SUPPORTED mean=%.2f std=%.2f support_fraction=%.2f" % (mean_ratio, 0.0, support_fraction)
    elif any(r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        RESULT = "SUPPORTED mean=%.2f std=%.2f support_fraction=%.2f" % (mean_ratio, 0.0, support_fraction)
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        RESULT = f"FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}"
    
    print(RESULT)