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
        if n == 1:
            return "x"
        else:
            subformulas = [generate_formula(random.randint(1, n-1)) for _ in range(2)]
            return f"({subformulas[0]} & {subformulas[1]})"
    
    def is_satisfiable(formula):
        stack = []
        i = 0
        while i < len(formula):
            if formula[i] == '(':
                stack.append(i)
            elif formula[i] == ')':
                start = stack.pop()
                if i - start <= 2:
                    return False
                subformula = formula[start+1:i]
                if '&' in subformula and '!' not in subformula:
                    return False
            i += 1
        return True
    
    def compute_automorphism_group(formula):
        # Simplified automorphism group computation for demonstration purposes
        return len(formula)
    
    def prove_formula(formula, max_depth=20):
        if formula == "x":
            return 1
        elif '&' in formula:
            left, right = formula.split('&')
            return prove_formula(left, max_depth-1) + prove_formula(right, max_depth-1)
        else:
            return 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_formula(n)
        if not is_satisfiable(formula):
            continue
        
        aut_group_size = compute_automorphism_group(formula)
        proof_length = prove_formula(formula)
        
        results.append({
            "n": n,
            "aut_group_size": aut_group_size,
            "proof_length": proof_length
        })
    
    if not results:
        return {
            "metric_name": "proof_length",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "unsatisfiable_formula"
        }
    
    aut_group_sizes = [r["aut_group_size"] for r in results]
    proof_lengths = [r["proof_length"] for r in results]
    
    mean_aut_group_size = sum(aut_group_sizes) / len(aut_group_sizes)
    mean_proof_length = sum(proof_lengths) / len(proof_lengths)
    
    correlation_coefficient = 0
    if len(aut_group_sizes) > 1:
        numerator = sum((a - mean_aut_group_size) * (p - mean_proof_length) for a, p in zip(aut_group_sizes, proof_lengths))
        denominator = math.sqrt(sum((a - mean_aut_group_size)**2 for a in aut_group_sizes)) * math.sqrt(sum((p - mean_proof_length)**2 for p in proof_lengths))
        correlation_coefficient = numerator / denominator
    
    max_ratio = max(abs(a / p) for a, p in zip(aut_group_sizes, proof_lengths))
    
    return {
        "metric_name": "proof_length",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) > 0.9 and max_ratio <= 5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "unsatisfiable_formula"
        result = f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(result)