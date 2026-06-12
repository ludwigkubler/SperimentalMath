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
    
    def generate_formula(n):
        if n == 1:
            return "x"
        else:
            subformulas = [generate_formula(random.randint(1, n-1)) for _ in range(2)]
            return f"({subformulas[0]} & {subformulas[1]})"
    
    def is_satisfiable(formula):
        if formula == "x":
            return True
        elif formula.startswith("(") and formula.endswith(")"):
            subformula = formula[1:-1]
            if subformula.startswith("(") and subformula.endswith(")"):
                left, right = subformula.split("&")
                return is_satisfiable(left) and is_satisfiable(right)
            else:
                return False
        else:
            return False
    
    def compute_automorphism_group(formula):
        if formula == "x":
            return {0}
        elif formula.startswith("(") and formula.endswith(")"):
            subformula = formula[1:-1]
            if subformula.startswith("(") and subformula.endswith(")"):
                left, right = subformula.split("&")
                automorphisms_left = compute_automorphism_group(left)
                automorphisms_right = compute_automorphism_group(right)
                return {0}
            else:
                return set()
        else:
            return set()
    
    def proof_length(formula):
        if formula == "x":
            return 1
        elif formula.startswith("(") and formula.endswith(")"):
            subformula = formula[1:-1]
            if subformula.startswith("(") and subformula.endswith(")"):
                left, right = subformula.split("&")
                return proof_length(left) + proof_length(right)
            else:
                return 0
        else:
            return 0
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        formula = generate_formula(n_max)
        if is_satisfiable(formula):
            automorphism_group = compute_automorphism_group(formula)
            proof_len = proof_length(formula)
            metric_values.append((len(automorphism_group), proof_len))
    
    if not metric_values:
        return {
            "metric_name": "proof_length",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "unsatisfiable_formula"
        }
    
    mean_aut = sum(x[0] for x in metric_values) / len(metric_values)
    mean_len = sum(x[1] for x in metric_values) / len(metric_values)
    max_ratio = max(abs(x[0] / x[1]) for x in metric_values if x[1] != 0)
    
    return {
        "metric_name": "proof_length",
        "metric_value": mean_aut,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": max_ratio <= 5 and len(metric_values) > 10,
        "counterexample": "" if max_ratio <= 5 else f"max_ratio={max_ratio}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_aut = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_aut) ** 2 for r in results if r["conjecture_holds"])) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_aut} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='max_ratio_exceeded' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_seeds_support")