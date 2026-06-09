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
    
    def dpll(clauses, assignment={}):
        if not clauses:
            return True
        var = next((v for v in range(1, max(variables) + 1) if v not in assignment), None)
        if var is None:
            return False
        
        pos_clauses = [c for c in clauses if any(v in c and assignment.get(v, False) for v in c)]
        neg_clauses = [c for c in clauses if any(v in c and not assignment.get(v, True) for v in c)]
        
        if dpll(pos_clauses, {**assignment, var: True}):
            return True
        elif dpll(neg_clauses, {**assignment, var: False}):
            return True
        
        return False
    
    def generate_cnf(n, m):
        variables = set(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            if random.choice([True, False]):
                clause = [-v for v in clause]
            clauses.append(tuple(sorted(clause)))
        return set(clauses)
    
    def categorical_representation(clauses):
        # Simplified representation using a dictionary to count morphisms
        morphisms = {}
        for clause in clauses:
            for var in clause:
                if var not in morphisms:
                    morphisms[var] = 1
                else:
                    morphisms[var] += 1
        return sum(morphisms.values())
    
    def dpll_search_tree_height(clauses):
        # Simplified DPLL search tree height calculation
        stack = [clauses]
        height = 0
        while stack:
            current_clauses = stack.pop()
            if not current_clauses:
                continue
            var = next((v for v in range(1, max(variables) + 1) if v not in {abs(c) for c in current_clauses}), None)
            if var is None:
                return height
            
            pos_clauses = [c for c in current_clauses if any(v in c and (assignment.get(v, False) if assignment else True) for v in c)]
            neg_clauses = [c for c in current_clauses if any(v in c and not (assignment.get(v, True) if assignment else False) for v in c)]
            
            stack.append(pos_clauses)
            stack.append(neg_clauses)
            height += 1
        
        return height
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            m = random.randint(n, 2 * n)
            clauses = generate_cnf(n, m)
            assignment = {}
            
            morphisms_count = categorical_representation(clauses)
            dpll_height = dpll_search_tree_height(clauses)
            
            results.append({
                "n": n,
                "m": m,
                "morphisms_count": morphisms_count,
                "dpll_height": dpll_height
            })
    
    if not results:
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = sum(r["morphisms_count"] / r["dpll_height"] for r in results) / len(results)
    instances_tested = len(results)
    n_max = max(r["n"] for r in results)
    
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": 0.5 <= ratio <= 1.5,
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
    
    if all(r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        std_ratio = (sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results)) ** 0.5
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")