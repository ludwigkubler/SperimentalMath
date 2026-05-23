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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] == -clause[j] for i in range(n) for j in range(i+1, n)):
                continue
            clauses.append(clause)
        return clauses
    
    def tropicalize(cnf):
        variables = set()
        for clause in cnf:
            for literal in clause:
                variables.add(abs(literal))
        return sorted(variables), cnf
    
    def galois_group_order(n):
        if n == 1: return 1
        if n % 2 == 0: return 2**(n-1)
        order = 1
        for i in range(3, n+1, 2):
            if n % i == 0:
                order *= i
        return order
    
    def dpll_search_tree_width(cnf):
        def backtrack(model, clause_index=0):
            if clause_index == len(cnf):
                return 1
            for literal in cnf[clause_index]:
                var = abs(literal)
                if literal > 0 and var not in model:
                    model[var] = True
                    width = backtrack(model, clause_index + 1)
                    if width > 0:
                        return width
                    del model[var]
                elif literal < 0 and var in model:
                    del model[var]
            return 0
        
        max_width = 0
        for assignment in itertools.product([True, False], repeat=len(variables)):
            model = {i+1: val for i, val in enumerate(assignment)}
            width = backtrack(model)
            if width > max_width:
                max_width = width
        return max_width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        variables, tropicalized_cnf = tropicalize(cnf)
        galois_order = galois_group_order(len(variables))
        width = dpll_search_tree_width(tropicalized_cnf)
        
        results.append({
            "n": n,
            "galois_order": galois_order,
            "width": width
        })
    
    mean_galois_order = sum(result["galois_order"] for result in results) / len(results)
    mean_width = sum(result["width"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["width"] <= 3 * result["galois_order"]) / len(results)
    
    return {
        "metric_name": "DPLL Search Tree Width vs Galois Group Order",
        "metric_value": mean_width,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"n={results[0]['n']}, galois_order={results[0]['galois_order']}, width={results[0]['width']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3**j for i in range(5) for j in range(5)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='n={results[0]['n']}, galois_order={results[0]['galois_order']}, width={results[0]['width']}' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")