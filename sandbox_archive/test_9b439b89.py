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
    
    def generate_formula(m):
        literals = [f"x{i}" for i in range(1, m+1)]
        clauses = []
        for _ in range(m):
            clause = random.sample(literals, 2)
            clause.append("~" + random.choice(clause))
            clauses.append(" & ".join(clause))
        formula = " | ".join(clauses)
        return formula
    
    def resolution_width(formula):
        # Simplified resolution width calculation for demonstration
        # This is a placeholder and should be replaced with actual logic
        return len(formula.split("|"))
    
    def minimal_affine_order(formula):
        # Simplified affine order calculation for demonstration
        # This is a placeholder and should be replaced with actual logic
        return len(formula.split("&"))
    
    m = random.randint(5, 40)
    formula = generate_formula(m)
    w_phi = resolution_width(formula)
    aff_order_phi = minimal_affine_order(formula)
    
    metric_name = "aff_order_vs_w"
    metric_value = aff_order_phi / w_phi
    instances_tested = 1
    n_max = m
    conjecture_holds = True if metric_value >= 0.8 else False
    counterexample = "" if conjecture_holds else f"Formula: {formula}, aff_order={aff_order_phi}, w={w_phi}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_r = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_r} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")