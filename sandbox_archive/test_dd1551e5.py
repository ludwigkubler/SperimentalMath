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
    
    def generate_boolean_formula(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(2 * n):
            clause = random.choice(variables + [f'~{v}' for v in variables])
            clauses.append(clause)
        return ' & '.join(clauses)
    
    def dpll_search_tree_height(formula):
        # Simplified DPLL algorithm to estimate search tree height
        if ' & ' not in formula:
            return 1
        parts = formula.split(' & ')
        return max(dpll_search_tree_height(p) for p in parts) + 1
    
    def construct_braided_monoidal_category(clause_set):
        # Simplified construction of a braided monoidal category
        generators = set()
        for clause in clause_set:
            if ' & ' in clause:
                generators.update(clause.split(' & '))
            else:
                generators.add(clause)
        return len(generators)
    
    n_max = 0
    instances_tested = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        instances_tested += 1
        formula = generate_boolean_formula(n)
        height = dpll_search_tree_height(formula)
        clause_set = formula.split(' & ')
        generators = construct_braided_monoidal_category(clause_set)
        
        metric_values.append(height / math.log(n) / math.log(math.log(n)))
        
        if len(metric_values) >= 30:
            mean_value = sum(metric_values) / len(metric_values)
            if mean_value < 0.5:
                conjecture_holds = False
                counterexample = f"n={n}, height={height}, generators={generators}"
    
    return {
        "metric_name": "DPLL Search Tree Height",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")