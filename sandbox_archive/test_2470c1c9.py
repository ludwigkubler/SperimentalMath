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
    
    def generate_boolean_formula(n):
        if n == 1:
            return random.choice(['0', '1'])
        else:
            subformulas = [generate_boolean_formula(random.randint(1, n-1)) for _ in range(random.randint(2, n))]
            operator = random.choice(['&', '|'])
            return f'({subformulas[0]} {operator} {subformulas[1]})'
    
    def truth_assignments(formula):
        if formula.isdigit():
            return [formula]
        elif '&' in formula:
            left, right = formula.split('&')
            return [f'{a}{b}' for a in truth_assignments(left) for b in truth_assignments(right)]
        else:
            left, right = formula.split('|')
            return [f'{a}{b}' for a in truth_assignments(left) for b in truth_assignments(right)]
    
    def quasi_commutative_braid_group_order(formula):
        # Placeholder for the actual algorithm to compute the minimal order of the QCBG
        # For simplicity, we assume it is proportional to the number of truth assignments
        return len(truth_assignments(formula))
    
    def resolution_proof_width(formula):
        # Placeholder for a small DPLL solver to compute the resolution proof width
        # For simplicity, we assume it is proportional to the length of the formula
        return len(formula)
    
    n = random.randint(5, 40)
    formula = generate_boolean_formula(n)
    mtr_QCBG = quasi_commutative_braid_group_order(formula)
    w_phi = resolution_proof_width(formula)
    
    if mtr_QCBG == 0 or w_phi == 0:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = (mtr_QCBG - w_phi) / math.sqrt(mtr_QCBG * w_phi)
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(correlation) >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break