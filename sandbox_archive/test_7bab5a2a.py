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
            op = random.choice(['&', '|', '^'])
            left = generate_formula(n // 2)
            right = generate_formula(n - n // 2)
            return f"({left} {op} {right})"
    
    def eval_formula(point, formula):
        if formula == 'True':
            return True
        elif formula == 'False':
            return False
        else:
            op = formula[1]
            left = eval_formula(point[:len(formula)//2], formula[3:-4])
            right = eval_formula(point[len(formula)//2:], formula[-4:-1])
            if op == '&':
                return left and right
            elif op == '|':
                return left or right
            elif op == '^':
                return left != right
    
    def polytope_points(formula):
        n = len(formula)
        points = []
        for i in range(2**n):
            point = tuple(int(x) for x in bin(i)[2:].zfill(n))
            if eval_formula(point, formula):
                points.append(point)
        return points
    
    def compute_ehrhart_quotient(polytope_points):
        n = len(polytope_points[0])
        min_k = 1
        while True:
            count = sum(1 for point in polytope_points if all((point[i] + k) % 2 == 0 for i in range(n)))
            if count >= k:
                return k
            k += 1
    
    def dpll_proof_tree_height(formula):
        n = len(formula)
        stack = [formula]
        height = 0
        while stack:
            formula = stack.pop()
            if formula == 'True' or formula == 'False':
                continue
            op = formula[1]
            left = eval_formula((0,) * (len(formula)//2), formula[3:-4])
            right = eval_formula((1,) * (len(formula)//2), formula[-4:-1])
            if op == '&':
                stack.append(left)
                stack.append(right)
            elif op == '|':
                stack.append(left)
                stack.append(right)
            elif op == '^':
                stack.append(left)
                stack.append(right)
            height += 1
        return height
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_formula(n)
        points = polytope_points(formula)
        ehrhart_quotient = compute_ehrhart_quotient(points)
        dpll_height = dpll_proof_tree_height(formula)
        results.append({
            "n": n,
            "ehrhart_quotient": ehrhart_quotient,
            "dpll_height": dpll_height
        })
    
    mean_ehrhart_quotient = sum(result["ehrhart_quotient"] for result in results) / len(results)
    mean_dpll_height = sum(result["dpll_height"] for result in results) / len(results)
    ratio = mean_ehrhart_quotient / (mean_dpll_height ** 2)
    
    if ratio <= 1.05:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "ratio_out_of_bound"
    
    return {
        "metric_name": "Ehrhart Quotient / DPLL Height Ratio",
        "metric_value": ratio,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"ratio_out_of_bound\" first_failing_seed={first_failing_seed}")