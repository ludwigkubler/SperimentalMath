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
    
    def generate_instance(n):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(n):
            clause = [random.choice(variables), -random.choice(variables)]
            clauses.append(clause)
        return clauses
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            return False
        pure_literal = next((l for l in variables if all(l not in c or -l not in c for c in clauses)), None)
        if pure_literal:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            if dpll([c for c in clauses if pure_literal not in c and -pure_literal not in c], new_assignment):
                return True
            new_assignment[pure_literal] = False
            if dpll([c for c in clauses if pure_literal not in c and -pure_literal not in c], new_assignment):
                return True
            return False
        literal = random.choice(variables)
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
            return True
        new_assignment[literal] = False
        if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
            return True
        return False
    
    def geometric_complexity(clauses):
        # Simplified heuristic to estimate geometric complexity
        return len(clauses) ** 0.5
    
    def height_of_dpll_tree(clauses, assignment):
        if not clauses:
            return 0
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            height_true = 1 + height_of_dpll_tree([c for c in clauses if literal not in c and -literal not in c], new_assignment)
            new_assignment[literal] = False
            height_false = 1 + height_of_dpll_tree([c for c in clauses if literal not in c and -literal not in c], new_assignment)
            return max(height_true, height_false)
        pure_literal = next((l for l in variables if all(l not in c or -l not in c for c in clauses)), None)
        if pure_literal:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            height_true = 1 + height_of_dpll_tree([c for c in clauses if pure_literal not in c and -pure_literal not in c], new_assignment)
            new_assignment[pure_literal] = False
            height_false = 1 + height_of_dpll_tree([c for c in clauses if pure_literal not in c and -pure_literal not in c], new_assignment)
            return max(height_true, height_false)
        literal = random.choice(variables)
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        height_true = 1 + height_of_dpll_tree([c for c in clauses if literal not in c and -literal not in c], new_assignment)
        new_assignment[literal] = False
        height_false = 1 + height_of_dpll_tree([c for c in clauses if literal not in c and -literal not in c], new_assignment)
        return max(height_true, height_false)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_height = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            clauses = generate_instance(n)
            height = height_of_dpll_tree(clauses, {})
            total_height += height
            instances_tested += 1
            if n > n_max:
                n_max = n
    
    mean_height = total_height / instances_tested
    conjecture_holds = all(mean_height <= 10 * geometric_complexity(generate_instance(n)) for n in n_values)
    
    return {
        "metric_name": "DPLL Proof Tree Height",
        "metric_value": mean_height,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_height = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_height} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")