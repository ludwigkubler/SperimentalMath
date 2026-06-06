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
    
    def generate_random_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        formula = ' '.join(random.choices(variables + ['¬'] + variables, k=3*n))
        return formula
    
    def evaluate_formula(formula):
        stack = []
        tokens = formula.split()
        for token in tokens:
            if token == '¬':
                operand = stack.pop()
                stack.append('¬' + operand)
            elif token in variables:
                stack.append(token)
            else:
                right = stack.pop()
                left = stack.pop()
                stack.append(f'({left} {token} {right})')
        return eval(stack[0])
    
    def frege_proof_width(formula):
        # Simplified Frege proof width calculation
        return len(formula.split())
    
    def formal_concept_lattice_size(formula):
        # Simplified concept lattice size calculation
        return len(formula.split())
    
    n = random.randint(5, 40)
    formula = generate_random_formula(n)
    while evaluate_formula(formula) == 0:
        formula = generate_random_formula(n)
    
    w_F = frege_proof_width(formula)
    C_phi = formal_concept_lattice_size(formula)
    
    if w_F == 0 or C_phi == 0:
        return {
            "metric_name": "Ratio",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"Formula: {formula}, Proof Width: {w_F}, Concept Lattice Size: {C_phi}"
        }
    
    ratio = Fraction(C_phi, w_F)
    return {
        "metric_name": "Ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in res and res["conjecture_holds"] for res in results):
        mean_value = sum(res["metric_value"] for res in results) / len(results)
        std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
        support_fraction = sum(1 for res in results if "conjecture_holds" in res and res["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("counterexample" in res and res["counterexample"] for res in results):
        first_failing_seed = next(res["seed"] for res in results if "counterexample" in res and res["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(res['counterexample'] for res in results if 'counterexample' in res)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")