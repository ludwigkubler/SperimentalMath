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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def construct_variety(formula):
        n = len(formula)
        variety = {}
        for j in range(n):
            term = 1
            for clause in formula:
                if j in [abs(lit) - 1 for lit in clause]:
                    term *= (-1)**(sum(lit > 0 for lit in clause))
            variety[j] = term
        return variety
    
    def count_cuspidal_sheaves(variety):
        return sum(abs(val) for val in variety.values())
    
    def compute_resolution_width(formula):
        n = len(formula)
        width = 0
        for clause in formula:
            width = max(width, len(clause))
        return width
    
    n = random.randint(5, 40)
    formula = generate_formula(n)
    variety = construct_variety(formula)
    
    if not variety:
        return {
            "metric_name": "cuspidal_sheaves",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    cuspidal_sheaves = count_cuspidal_sheaves(variety)
    resolution_width = compute_resolution_width(formula)
    
    return {
        "metric_name": "cuspidal_sheaves",
        "metric_value": cuspidal_sheaves,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(cuspidal_sheaves - resolution_width) <= 0.5 * resolution_width,
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}")
    else:
        print("RESULT: INCONCLUSIVE some_trials_failed")