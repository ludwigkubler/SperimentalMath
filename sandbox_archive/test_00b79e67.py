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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def dpll_solver(f, n):
    def solve(vars, assignment):
        if len(assignment) == n:
            if all(f[i] == evaluate_expression(i, assignment) for i in range(2**n)):
                return True
            else:
                return False
        var = vars[0]
        for val in [0, 1]:
            new_assignment = assignment + [(var, val)]
            if solve(vars[1:], new_assignment):
                return True
        return False
    
    vars = list(range(n))
    return solve(vars, [])

def evaluate_expression(i, assignment):
    n = len(assignment)
    expr = i
    for j in range(n):
        if expr & (1 << j):
            expr ^= assignment[j]
    return expr

def construct_affine_plane_curve(f, n):
    curve = []
    for i in range(2**n):
        curve.append((i, f[i]))
    return curve

def min_degree(curve):
    x_coords = [p[0] for p in curve]
    y_coords = [p[1] for p in curve]
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def extended_gcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, x, y = extended_gcd(b % a, a)
            return (g, y - (b // a) * x, x)
    
    def line_equation(p1, p2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        gcd_val = abs(gcd(dx, dy))
        return (dx // gcd_val, dy // gcd_val, p1[0] * dy - p1[1] * dx)
    
    def is_collinear(p1, p2, p3):
        eq1 = line_equation(p1, p2)
        eq2 = line_equation(p1, p3)
        return eq1 == eq2
    
    for i in range(len(curve)):
        for j in range(i + 1, len(curve)):
            for k in range(j + 1, len(curve)):
                if is_collinear(curve[i], curve[j], curve[k]):
                    return None
    return max([max(abs(p[0]), abs(p[1])) for p in curve])

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_boolean_function(n)
    
    if not dpll_solver(f, n):
        return {
            "metric_name": "communication_complexity",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "function_is_not_sat"
        }
    
    curve = construct_affine_plane_curve(f, n)
    degree = min_degree(curve)
    
    if degree is None:
        return {
            "metric_name": "communication_complexity",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "curve_is_not_affine"
        }
    
    communication_complexity = dpll_solver(f, n)
    return {
        "metric_name": "communication_complexity",
        "metric_value": communication_complexity,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"function_is_not_sat\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")