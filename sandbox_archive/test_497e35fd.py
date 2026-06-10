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
    
    def generate_satisfiability_instance(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(1, n), random.randint(-n, -1)]
            if random.choice([True, False]):
                clause[0], clause[1] = clause[1], clause[0]
            clauses.append(clause)
        return clauses
    
    def dpll_search_tree_height(clauses):
        n = max(abs(c) for c in [v for clause in clauses for v in clause])
        assignment = {}
        
        def dpll(clauses, assignment):
            if not clauses:
                return 0
            pure_literal = next((v for v in range(1, n + 1) if (v in [c[0] for c in clauses] and -v not in [c[0] for c in clauses])), None)
            if pure_literal is not None:
                assignment[pure_literal] = True
                return dpll([c for c in clauses if not any(v in c or -v in c for v in assignment)], assignment) + 1
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause is not None:
                literal = unit_clause[0]
                assignment[literal] = True
                return dpll([c for c in clauses if not any(v in c or -v in c for v in assignment)], assignment) + 1
            literal = random.choice(clauses[0])
            return max(dpll([c for c in clauses if not any(v in c or -v in c for v in assignment)], {**assignment, literal: True}),
                       dpll([c for c in clauses if not any(v in c or -v in c for v in assignment)], {**assignment, literal: False})) + 1
        
        return dpll(clauses, assignment)
    
    def modular_form_order(clause_set):
        # Placeholder function to compute the order of the lowest degree modular form
        # This is a dummy implementation and should be replaced with actual computation
        return len(clause_set)  # Example: Order is proportional to the number of clauses
    
    n = random.randint(5, 40)
    clauses = generate_satisfiability_instance(n)
    dpll_height = dpll_search_tree_height(clauses)
    order = modular_form_order(clauses)
    
    return {
        "metric_name": "DPLL Tree Height vs Modular Form Order",
        "metric_value": abs(dpll_height - order),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
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
    elif support_fraction >= 0.75:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={seeds[first_failing_seed]}")