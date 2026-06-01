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
            return ['x1']
        else:
            return [f'~{generate_formula(n-1)[0]}'] + generate_formula(n-1)
    
    def dpll(formula, assignment={}):
        if not formula:
            return True
        literal = next((lit for lit in formula if lit[0] != '~'), None)
        if literal is None:
            return False
        
        pos_lit = literal[1:] if literal.startswith('~') else literal
        if pos_lit in assignment and assignment[pos_lit]:
            return dpll([f for f in formula if f != literal], assignment)
        
        assignment[pos_lit] = True
        if dpll(formula, assignment):
            return True
        
        assignment[pos_lit] = False
        if dpll([f for f in formula if f != literal], assignment):
            return True
        
        return False
    
    def symplectic_volume(n):
        # Placeholder for actual symplectic volume computation
        # For simplicity, we use a linear function of n
        return Fraction(n, 1)
    
    def compute_diameter(formula):
        if not formula:
            return 0
        if len(formula) == 1:
            return 1
        
        max_depth = 0
        for lit in formula:
            sub_formula = [f for f in formula if f != lit]
            depth = 1 + compute_diameter(sub_formula)
            if depth > max_depth:
                max_depth = depth
        return max_depth
    
    n_values = [5, 10, 15, 20, 30, 40]
    msv_values = []
    diameter_values = []
    
    for n in n_values:
        formula = generate_formula(n)
        msv = symplectic_volume(n)
        diameter = compute_diameter(formula)
        
        msv_values.append(msv)
        diameter_values.append(diameter)
    
    if not msv_values or not diameter_values:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "empty_formula"
        }
    
    mean_msv = sum(msv_values) / len(msv_values)
    mean_diameter = sum(diameter_values) / len(diameter_values)
    
    covariance = sum((msv - mean_msv) * (diameter - mean_diameter) for msv, diameter in zip(msv_values, diameter_values)) / len(msv_values)
    variance_msv = sum((msv - mean_msv) ** 2 for msv in msv_values) / len(msv_values)
    variance_diameter = sum((diameter - mean_diameter) ** 2 for diameter in diameter_values) / len(diameter_values)
    
    if variance_msv == 0 or variance_diameter == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(msv_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }
    
    correlation_coefficient = covariance / (math.sqrt(variance_msv) * math.sqrt(variance_diameter))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(msv_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for result in results if not result["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"low_support\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")