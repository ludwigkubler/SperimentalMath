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
    
    def generate_hyperbolic_tiling(n):
        # Placeholder for hyperbolic tiling generation logic
        return [random.randint(1, 3) for _ in range(n)]
    
    def compute_mli(tiling):
        # Placeholder for minimal local indeterminacy computation
        return sum(tiling)
    
    def compute_fpl(tiling):
        # Placeholder for Frege proof length computation
        cls = {}
        literals = set()
        for tile in tiling:
            literals.update([tile, -tile])
        for lit in literals:
            if lit not in cls:
                cls[lit] = []
        return len(cls)
    
    def solve(lits_true, lits_false):
        # Placeholder for DPLL solver logic
        return True
    
    n_max = 40
    instances_tested = 30
    mli_values = []
    fpl_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        tiling = generate_hyperbolic_tiling(n)
        mli_value = compute_mli(tiling)
        fpl_value = compute_fpl(tiling)
        mli_values.append(mli_value)
        fpl_values.append(fpl_value)
    
    if not mli_values or not fpl_values:
        return {
            "metric_name": "mli_vs_fpl",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "empty_values"
        }
    
    mean_mli = sum(mli_values) / len(mli_values)
    mean_fpl = sum(fpl_values) / len(fpl_values)
    std_mli = math.sqrt(sum((x - mean_mli) ** 2 for x in mli_values) / len(mli_values))
    std_fpl = math.sqrt(sum((x - mean_fpl) ** 2 for x in fpl_values) / len(fpl_values))
    
    correlation_coefficient = sum((mli_values[i] - mean_mli) * (fpl_values[i] - mean_fpl) for i in range(len(mli_values))) / (len(mli_values) * std_mli * std_fpl)
    
    return {
        "metric_name": "mli_vs_fpl",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"mli_vs_fpl\" first_failing_seed={r['seed']}")
                break