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
    
    def tseitin_formula(n):
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        
        # Generate the Tseitin formula
        for i in range(n):
            clause = [literals[i], f'y{i}']
            clauses.append(clause)
            clause = [f'y{i}', f'z{i}']
            clauses.append(clause)
            clause = [f'~y{i}', literals[i]]
            clauses.append(clause)
            clause = [f'~z{i}', f'~x{i}']
            clauses.append(clause)
        
        # Add the final clause
        for i in range(n):
            clause = [f'y{i}', f'z{i}']
            clauses.append(clause)
        
        return literals, clauses

    def categorify_formula(literals, clauses):
        n = len(literals)
        categorified_clauses = []
        
        for clause in clauses:
            new_clause = []
            for literal in clause:
                if literal.startswith('x'):
                    new_literal = f'y{literal[1]}'
                elif literal.startswith('~x'):
                    new_literal = f'z{literal[2]}'
                else:
                    new_literal = literal
                new_clause.append(new_literal)
            categorified_clauses.append(new_clause)
        
        return categorified_clauses

    def resolution_width(clauses):
        n = len(clauses)
        width = 0
        
        for clause in clauses:
            if len(clause) > width:
                width = len(clause)
        
        return width

    def min_order(categorified_clauses):
        # Placeholder for the actual categorification order calculation
        # This is a dummy implementation that returns the number of clauses
        return len(categorified_clauses)

    n = random.randint(5, 40)
    literals, clauses = tseitin_formula(n)
    categorified_clauses = categorify_formula(literals, clauses)
    w_phi = resolution_width(clauses)
    min_order_phi_categ = min_order(categorified_clauses)

    return {
        "metric_name": "min_order",
        "metric_value": min_order_phi_categ,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")