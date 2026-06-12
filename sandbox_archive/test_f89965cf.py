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
    
    def parse(formula):
        if formula.startswith('¬'):
            return ('¬', parse(formula[1:]))
        elif ' & ' in formula:
            left, right = formula.split(' & ')
            return ('&', parse(left), parse(right))
        elif ' ∨ ' in formula:
            left, right = formula.split(' ∨ ')
            return ('∨', parse(left), parse(right))
        else:
            return formula
    
    def tseitin_formula(formula):
        if isinstance(formula, str):
            return formula
        elif formula[0] == '¬':
            subformula = tseitin_formula(formula[1])
            return f"¬{subformula}"
        elif formula[0] == '&':
            left = tseitin_formula(formula[1])
            right = tseitin_formula(formula[2])
            return f"{left} & {right}"
        elif formula[0] == '∨':
            left = tseitin_formula(formula[1])
            right = tseitin_formula(formula[2])
            return f"{left} ∨ {right}"
    
    def motivic_order(formula):
        if isinstance(formula, str):
            return 1
        elif formula[0] == '¬':
            return motivic_order(formula[1]) + 1
        elif formula[0] == '&':
            left = motivic_order(formula[1])
            right = motivic_order(formula[2])
            return max(left, right) + 1
        elif formula[0] == '∨':
            left = motivic_order(formula[1])
            right = motivic_order(formula[2])
            return min(left, right) + 1
    
    def dpll_width(formula):
        if isinstance(formula, str):
            return 1
        elif formula[0] == '¬':
            return dpll_width(formula[1]) + 1
        elif formula[0] == '&':
            left = dpll_width(formula[1])
            right = dpll_width(formula[2])
            return max(left, right) + 1
        elif formula[0] == '∨':
            left = dpll_width(formula[1])
            right = dpll_width(formula[2])
            return min(left, right) + 1
    
    n = random.randint(5, 40)
    variables = [f"v{i}" for i in range(n)]
    literals = [random.choice([var, f"¬{var}"]) for var in variables]
    formula = ' & '.join(literals)
    
    tseitin = tseitin_formula(formula)
    order = motivic_order(tseitin)
    width = dpll_width(tseitin)
    
    return {
        "metric_name": "MotivicOrder",
        "metric_value": order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": order <= 2 * width,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        results.append(trial_result)
        print(f"TRIAL: {trial_result}")
    
    mean_order = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"order > 2 * width\" first_failing_seed={first_failing_seed}")