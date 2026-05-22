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
    
    def generate_formula(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def integral_representation(formula):
        n = len(formula)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            matrix[i][i] = formula[i]
            matrix[n][i] = -formula[i]
        matrix[n][n] = 1
        return gaussian_elimination(matrix)
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            if A[i][i] == 0:
                for j in range(i + 1, n):
                    if A[j][i] != 0:
                        A[i], A[j] = A[j], A[i]
                        break
                else:
                    return None  # Singular matrix
            for j in range(n):
                if j != i and A[j][i] != 0:
                    factor = -A[j][i] / A[i][i]
                    for k in range(n + 1):
                        A[j][k] += factor * A[i][k]
        return A
    
    def norm(matrix):
        n = len(matrix)
        max_val = 0
        for i in range(n):
            for j in range(n + 1):
                if abs(matrix[i][j]) > max_val:
                    max_val = abs(matrix[i][j])
        return max_val
    
    def dpll_search_tree_width(formula):
        n = len(formula)
        stack = [(0, [])]
        while stack:
            i, assignment = stack.pop()
            if i == n:
                return len(assignment)
            for j in range(n):
                if formula[j] != assignment[j]:
                    new_assignment = assignment[:]
                    new_assignment.append(formula[j])
                    stack.append((i + 1, new_assignment))
        return float('inf')
    
    n = random.randint(5, 40)
    formula = generate_formula(n)
    integral_rep = integral_representation(formula)
    if integral_rep is None:
        return {
            "metric_name": "Minimal Norm",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Singular matrix"
        }
    
    minimal_norm = norm(integral_rep)
    search_tree_width = dpll_search_tree_width(formula)
    
    return {
        "metric_name": "Minimal Norm",
        "metric_value": minimal_norm,
        "instances_tested": 1,
        "conjecture_holds": minimal_norm <= math.log(n) and search_tree_width <= 2 * math.log(n),
        "counterexample": "" if minimal_norm <= math.log(n) and search_tree_width <= 2 * math.log(n) else f"Minimal norm: {minimal_norm}, Search tree width: {search_tree_width}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")