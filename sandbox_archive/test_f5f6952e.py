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
    
    def generate_formula(n):
        return ''.join(random.choice('01') for _ in range(2**n))
    
    def compute_ehrhart_quotient(polytope_points):
        if not polytope_points:
            return 0
        min_k = float('inf')
        for point in polytope_points:
            k = sum(point) + 1
            if k < min_k:
                min_k = k
        return min_k
    
    def dpll_formula(formula, assignment=[]):
        if not formula:
            return True
        var = formula[0]
        rest = formula[2:]
        if var in assignment:
            if assignment[var] == (rest[1] == '1'):
                return dpll_formula(rest[3:], assignment)
            else:
                return False
        for val in [True, False]:
            assignment[var] = val
            if dpll_formula(rest, assignment):
                return True
            del assignment[var]
        return False
    
    def polytope_points(formula):
        n = formula.count('0') + formula.count('1')
        points = []
        for i in range(2**n):
            point = [int(bit) for bit in format(i, f'0{n}b')]
            if eval_formula(point, formula):
                points.append(point)
        return points
    
    def eval_formula(point, formula):
        stack = []
        i = 0
        while i < len(formula):
            if formula[i] == '0':
                stack.append(not point[eval_formula(point[:i], formula)])
                i += 1
            elif formula[i] == '1':
                stack.append(point[eval_formula(point[:i], formula)])
                i += 1
            elif formula[i] == '(':
                j = i + 1
                while formula[j] != ')':
                    j += 1
                subformula = formula[i+1:j]
                stack.append(eval_formula(point, subformula))
                i = j + 1
            else:
                stack.append(point[eval_formula(point[:i], formula)])
                i += 1
        return stack[-1]
    
    def dpll_proof_tree_height(formula):
        if not formula:
            return 0
        var = formula[0]
        rest = formula[2:]
        return max(dpll_proof_tree_height(rest), dpll_proof_tree_height(rest[3:])) + 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_formula(n)
        points = polytope_points(formula)
        ehrhart_quotient = compute_ehrhart_quotient(points)
        dpll_height = dpll_proof_tree_height(formula)
        if ehrhart_quotient == 0 or dpll_height == 0:
            continue
        results.append((ehrhart_quotient, dpll_height))
    
    if not results:
        return {
            "metric_name": "Ehrhart Quotient / DPLL Proof Tree Height Ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid results for any n"
        }
    
    ehrhart_quotients = [r[0] for r in results]
    dpll_heights = [r[1] for r in results]
    
    ratio = sum(e / (d ** 2) for e, d in zip(ehrhart_quotients, dpll_heights)) / len(results)
    conjecture_holds = all(0.95 <= e / (d ** 2) <= 1.05 for e, d in zip(ehrhart_quotients, dpll_heights))
    
    return {
        "metric_name": "Ehrhart Quotient / DPLL Proof Tree Height Ratio",
        "metric_value": ratio,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "Ratio out of bounds"
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
        mean = sum(r["metric_value"] for r in results) / len(results)
        std = (sum((r["metric_value"] - mean) ** 2 for r in results) / len(results)) ** 0.5
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no valid results")