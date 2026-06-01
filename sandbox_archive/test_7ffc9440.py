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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses

    def polynomial_value(poly, x):
        result = 0
        for coeff in poly:
            result = (result * x + coeff) % m
        return result

    def minimal_local_ring_norm(formula, m):
        poly = [1]  # Constant term
        for clause in formula:
            term = 1
            for var in clause:
                if var > 0:
                    term *= (x**var - 1)
                else:
                    term *= (x**(-var) - 1)
            poly.append(term)
        
        min_norm = float('inf')
        for i in range(2, m):
            val = polynomial_value(poly, i)
            if val < min_norm:
                min_norm = val
        return min_norm

    def dpll_search_tree(formula):
        def dfs(model, clause_index):
            if clause_index == len(formula):
                return True
            for literal in formula[clause_index]:
                if literal > 0 and literal not in model:
                    model.add(literal)
                    if dfs(model, clause_index + 1):
                        return True
                    model.remove(literal)
                elif literal < 0 and -literal in model:
                    if dfs(model, clause_index + 1):
                        return True
            return False
        
        model = set()
        return len(formula) - sum(1 for _ in filter(dfs, [model]))

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(n**2, 2*n**2)
        formula = generate_cnf(n)
        
        min_norm = minimal_local_ring_norm(formula, m)
        tree_diameter = dpll_search_tree(formula)
        
        if min_norm == float('inf'):
            continue
        
        results.append({
            "n": n,
            "min_norm": min_norm,
            "tree_diameter": tree_diameter
        })
    
    if not results:
        return {
            "metric_name": "min_norm vs diameter",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_norms = [r["min_norm"] for r in results]
    diameters = [r["tree_diameter"] for r in results]
    
    n_max = max(r["n"] for r in results)
    instances_tested = len(results)
    conjecture_holds = all(min_norm >= 0.7 * diameter for min_norm, diameter in zip(min_norms, diameters))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_norm vs diameter",
        "metric_value": sum(min_norms) / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(r["conjecture_holds"] for r in results):
        counterexample = next((r["counterexample"] for r in results if r["counterexample"]), "mapping_undefined")
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")