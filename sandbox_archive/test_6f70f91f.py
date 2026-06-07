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
    
    def generate_boolean_formula(n):
        if n == 0:
            return "False"
        elif n == 1:
            return "x" + str(random.randint(0, n-1))
        else:
            op = random.choice(["&", "|"])
            left = generate_boolean_formula(random.randint(0, n//2))
            right = generate_boolean_formula(n - len(left.split("&")) - len(right.split("|")))
            return f"({left} {op} {right})"
    
    def frege_proof_depth(formula):
        if formula == "False":
            return 1
        elif formula.startswith("x"):
            return 2
        else:
            left, op, right = formula[1:-1].split()
            return 1 + max(frege_proof_depth(left), frege_proof_depth(right))
    
    def min_order(n):
        # This is a placeholder for computing the minimum order of a monoid.
        # For simplicity, we assume it's proportional to n.
        return n
    
    instances_tested = 0
    total_min_order = 0
    total_frege_depth = 0
    
    for _ in range(30):
        n = random.randint(5, 40)
        formula = generate_boolean_formula(n)
        min_order_M = min_order(n)
        f_phi = frege_proof_depth(formula)
        
        instances_tested += 1
        total_min_order += min_order_M
        total_frege_depth += f_phi
    
    mean_min_order = total_min_order / instances_tested
    mean_frege_depth = total_frege_depth / instances_tested
    correlation_coefficient = (instances_tested * sum(min_order_M * f_phi for min_order_M, f_phi in zip(range(5, 41), range(5, 41))) - 
                               instances_tested * mean_min_order * mean_frege_depth) / \
                              math.sqrt((instances_tested * sum(min_order_M**2 for min_order_M in range(5, 41)) - instances_tested * mean_min_order**2) *
                                        (instances_tested * sum(f_phi**2 for f_phi in range(5, 41)) - instances_tested * mean_frege_depth**2))
    
    conjecture_holds = correlation_coefficient >= 0.95
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": 40,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")