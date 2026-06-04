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
            return random.choice(['True', 'False'])
        else:
            op = random.choice(['&', '|'])
            left = generate_formula(n // 2)
            right = generate_formula(n - len(left) - 3)
            return f"({left} {op} {right})"
    
    def eval_formula(point, formula):
        if formula == 'True':
            return True
        elif formula == 'False':
            return False
        else:
            op = formula[1]
            left = eval_formula(point[:len(formula)//2], formula[3:-4])
            right = eval_formula(point[len(formula)//2 + 2:], formula[len(formula)//2 + 5:])
            if op == '&':
                return left and right
            elif op == '|':
                return left or right
    
    def polytope_points(formula):
        n = len(formula)
        points = []
        for i in range(2**n):
            point = bin(i)[2:].zfill(n)
            if eval_formula(point, formula):
                points.append(tuple(map(int, point)))
        return points
    
    def compute_ehrhart_quotient(polytope_points):
        n = len(polytope_points)
        k = 1
        while True:
            if len(set(k * p for p in polytope_points)) >= n**2:
                return k
            k += 1
    
    def dpll_proof_tree_height(formula):
        if formula == 'True':
            return 0
        elif formula == 'False':
            return float('inf')
        else:
            op = formula[1]
            left = dpll_proof_tree_height(formula[3:-4])
            right = dpll_proof_tree_height(formula[len(formula)//2 + 5:])
            if op == '&':
                return max(left, right)
            elif op == '|':
                return min(left, right) + 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        formula = generate_formula(n)
        points = polytope_points(formula)
        ehrhart_quotient = compute_ehrhart_quotient(points)
        dpll_height = dpll_proof_tree_height(formula)
        
        if ehrhart_quotient == 0 or dpll_height == float('inf'):
            continue
        
        instances_tested += len(points)
        n_max = max(n_max, n)
        total_metric_value += Fraction(ehrhart_quotient**2, dpll_height)
        
        if ehrhart_quotient / dpll_height > 1.05:
            conjecture_holds = False
            counterexample = f"Formula: {formula}, Ehrhart Quotient: {ehrhart_quotient}, DPLL Height: {dpll_height}"
    
    return {
        "metric_name": "Ehrhart Quotient / DPLL Proof Tree Height Ratio",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")