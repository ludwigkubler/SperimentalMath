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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(10 * n):  # Generate 10 clauses per variable on average
            clause = [random.randint(-n, n) for _ in range(random.randint(2, n))]
            cnf.append(clause)
        return cnf
    
    def grothendieck_witt_class(cnf):
        m = len(cnf)
        n = max(abs(x) for x in sum(cnf, []))
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for x in clause:
                A[x][x] += 1
        return A
    
    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = Fraction(0)
        sign = 1
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += sign * A[0][j] * determinant(submatrix)
            sign *= -1
        return det
    
    def hodge_norm(A):
        det_A = determinant(A)
        if det_A == 0:
            return Fraction(0)
        return abs(det_A) ** (Fraction(1, n))
    
    def resolution_width(cnf):
        stack = []
        assignment = {}
        for clause in cnf:
            found_unassigned = False
            for literal in clause:
                if literal not in assignment and -literal not in assignment:
                    assignment[literal] = True
                    found_unassigned = True
                    break
            if not found_unassigned:
                stack.append(clause)
        width = 0
        while stack:
            clause = stack.pop()
            new_assignment = {}
            for literal in clause:
                if literal not in assignment and -literal not in assignment:
                    new_assignment[literal] = True
                    break
            if not new_assignment:
                return width
            width += 1
            for literal, value in new_assignment.items():
                assignment[literal] = value
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        A = grothendieck_witt_class(cnf)
        norm = hodge_norm(A)
        width = resolution_width(cnf)
        results.append((norm, width))
    
    if len(results) < 100:
        return {
            "metric_name": "Hodge Norm vs Resolution Width",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances"
        }
    
    norms = [norm for norm, _ in results]
    widths = [width for _, width in results]
    mean_norm = sum(norms) / len(norms)
    mean_width = sum(widths) / len(widths)
    corr_coeff = sum((norm - mean_norm) * (width - mean_width) for norm, width in results) / (len(results) * mean_norm * mean_width)
    
    return {
        "metric_name": "Hodge Norm vs Resolution Width",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": corr_coeff > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "First failing seed"
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(result['conjecture_holds'] for result in results) else 'FALSIFIED'} mean={mean_value} std={std_value} support_fraction={support_fraction}")