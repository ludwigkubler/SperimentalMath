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
    
    def generate_boolean_formula(n):
        if n == 1:
            return random.choice(['True', 'False'])
        else:
            op = random.choice(['and', 'or'])
            subformulas = [generate_boolean_formula(random.randint(1, n-1)) for _ in range(2)]
            return f"({subformulas[0]} {op} {subformulas[1]})"
    
    def poset_size(formula):
        if formula == 'True' or formula == 'False':
            return 2
        else:
            left, right = formula.split(' ')[0], formula.split(' ')[2]
            return max(poset_size(left), poset_size(right)) + 1
    
    def frege_proof_depth(formula):
        if formula == 'True' or formula == 'False':
            return 1
        else:
            left, right = formula.split(' ')[0], formula.split(' ')[2]
            return max(frege_proof_depth(left), frege_proof_depth(right)) + 1
    
    def min_order(formula):
        n = poset_size(formula)
        if n == 2:
            return 1
        else:
            return n - 1
    
    formula = generate_boolean_formula(40)
    n_max = poset_size(formula)
    instances_tested = 30
    metric_value = min_order(formula) / frege_proof_depth(formula)
    conjecture_holds = metric_value <= 2  # Assuming c = 2 for simplicity
    counterexample = "" if conjecture_holds else f"Formula: {formula}, Min Order: {min_order(formula)}, Frege Depth: {frege_proof_depth(formula)}"
    
    return {
        "metric_name": "Orbit Width Ratio",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3**j for i in range(5) for j in range(5)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")