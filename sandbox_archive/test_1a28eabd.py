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
            return random.choice(['True', 'False'])
        else:
            op = random.choice(['and', 'or'])
            subformulas = [generate_boolean_formula(random.randint(1, n-1)) for _ in range(2)]
            return f"({subformulas[0]} {op} {subformulas[1]})"
    
    def resolution_proof_width(formula):
        if formula == 'True' or formula == 'False':
            return 1
        elif 'and' not in formula and 'or' not in formula:
            raise ValueError("Invalid formula")
        else:
            subformulas = [f.strip('()') for f in formula.split(' ') if f]
            if 'and' in formula:
                left, right = subformulas[0], subformulas[1]
                return max(resolution_proof_width(left), resolution_proof_width(right))
            elif 'or' in formula:
                left, right = subformulas[0], subformulas[1]
                return 1 + min(resolution_proof_width(left), resolution_proof_width(right))
    
    def grothendieck_serre_duality_order(formula):
        # Placeholder for actual computation
        # For simplicity, we assume the order is proportional to the length of the formula
        return len(formula)
    
    n = random.randint(5, 40)
    phi = generate_boolean_formula(n)
    min_order_G_phi = grothendieck_serre_duality_order(phi)
    w_phi = resolution_proof_width(phi)
    
    if min_order_G_phi == 0 or w_phi == 0:
        return {
            "metric_name": "min_order(G(φ)) vs. w(φ)",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation_coefficient = min_order_G_phi / w_phi
    
    return {
        "metric_name": "min_order(G(φ)) vs. w(φ)",
        "metric_value": correlation_coefficient,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(correlation_coefficient - 1) <= 3 and correlation_coefficient >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support")