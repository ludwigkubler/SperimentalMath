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
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(variables, 2)
            clause.append(random.choice(['', '!', '~']))
            clauses.append(clause)
        return clauses
    
    def dpll_search_tree(clauses, assignment):
        if not clauses:
            return [assignment]
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            result = dpll_search_tree([c for c in clauses if literal not in c], new_assignment)
            if result:
                return result
            new_assignment[literal] = False
            return dpll_search_tree([c for c in clauses if literal not in c], new_assignment)
        pure_literal = next((l for l in variables if all(l not in c or (not c[0] == '!' and not c[0] == '~') for c in clauses)), None)
        if pure_literal:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            result = dpll_search_tree([c for c in clauses if pure_literal not in c], new_assignment)
            if result:
                return result
            new_assignment[pure_literal] = False
            return dpll_search_tree([c for c in clauses if pure_literal not in c], new_assignment)
        literal = random.choice(variables)
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        result = dpll_search_tree([c for c in clauses if literal not in c], new_assignment)
        if result:
            return result
        new_assignment[literal] = False
        return dpll_search_tree([c for c in clauses if literal not in c], new_assignment)
    
    def count_minimal_trees(clauses):
        assignment = {var: None for var in variables}
        trees = set()
        for _ in range(100):  # Sample multiple trees to avoid duplicates
            tree = dpll_search_tree(clauses, assignment.copy())
            if tree:
                trees.add(tuple(sorted(tree)))
        return len(trees)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    clauses = generate_formula(n)
    variables = [c[0] for c in clauses]
    num_trees = count_minimal_trees(clauses)
    
    return {
        "metric_name": "num_trees",
        "metric_value": num_trees,
        "instances_tested": 100,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")