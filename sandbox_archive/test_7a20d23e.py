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
            left = generate_boolean_formula(n // 2)
            right = generate_boolean_formula(n - n // 2)
            return f'({left} {op} {right})'
    
    def frege_proof_depth(formula):
        if formula == 'True' or formula == 'False':
            return 1
        else:
            op = formula[1]
            left = frege_proof_depth(formula[3:-1])
            right = frege_proof_depth(formula[5:-1])
            return max(left, right) + 1
    
    def count_symplectic_leaves(formula):
        if formula == 'True' or formula == 'False':
            return 0
        else:
            op = formula[1]
            left = count_symplectic_leaves(formula[3:-1])
            right = count_symplectic_leaves(formula[5:-1])
            return left + right + 1
    
    n_max = 40
    instances_tested = 0
    total_L = 0
    total_d = 0
    squared_total_L = 0
    squared_total_d = 0
    Ld_product = 0
    
    for n in range(5, n_max + 1):
        formula = generate_boolean_formula(n)
        d = frege_proof_depth(formula)
        L = count_symplectic_leaves(formula)
        
        instances_tested += 1
        total_L += L
        total_d += d
        squared_total_L += L ** 2
        squared_total_d += d ** 2
        Ld_product += L * d
    
    mean_L = Fraction(total_L, instances_tested)
    mean_d = Fraction(total_d, instances_tested)
    variance_L = Fraction(squared_total_L - instances_tested * mean_L ** 2, instances_tested)
    variance_d = Fraction(squared_total_d - instances_tested * mean_d ** 2, instances_tested)
    covariance_LD = Fraction(Ld_product - instances_tested * mean_L * mean_d, instances_tested)
    
    if variance_L == 0 or variance_d == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }
    
    correlation_coefficient = covariance_LD / (math.sqrt(variance_L) * math.sqrt(variance_d))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")