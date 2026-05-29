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
    
    def generate_random_kcnf(n, k):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(k):
            clause = set(random.sample(variables, random.randint(1, n)))
            if len(clause) == 1:
                clause.add(-list(clause)[0])
            clauses.append(tuple(sorted(clause)))
        return clauses
    
    def dpll_tree_depth(instance):
        variables = list(range(1, len(instance[0]) + 1))
        clauses = set(instance)
        
        def dpll(variables, assignment):
            if not clauses:
                return 0
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause is not None:
                literal = unit_clause[0]
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                if literal < 0:
                    new_assignment[-literal] = False
                return dpll(variables, new_assignment) + 1
            pure_literal = next((v for v in variables if all(v not in c or -v not in c for c in clauses)), None)
            if pure_literal is not None:
                new_assignment = assignment.copy()
                new_assignment[pure_literal] = True
                return dpll(variables, new_assignment) + 1
            literal = random.choice(variables)
            new_assignment_true = assignment.copy()
            new_assignment_true[literal] = True
            new_assignment_false = assignment.copy()
            new_assignment_false[literal] = False
            return max(dpll(variables, new_assignment_true), dpll(variables, new_assignment_false)) + 1
        
        return dpll(variables, {})
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_depth = 0
    instances_tested = 0
    
    for n in n_values:
        k = random.randint(1, min(n * (n - 1) // 2, 10))
        instance = generate_random_kcnf(n, k)
        depth = dpll_tree_depth(instance)
        total_depth += depth
        instances_tested += 1
    
    mean_depth = Fraction(total_depth, instances_tested)
    std_dev = 0
    for n in n_values:
        k = random.randint(1, min(n * (n - 1) // 2, 10))
        instance = generate_random_kcnf(n, k)
        depth = dpll_tree_depth(instance)
        std_dev += (depth - mean_depth) ** 2
    std_dev = math.sqrt(std_dev / instances_tested)
    
    C_n = Fraction(3, 1)  # Example constant, adjust as needed
    expected_bound = C_n * sum(n * math.log(n) for n in n_values) / len(n_values)
    
    if mean_depth > expected_bound + 3 * std_dev:
        conjecture_holds = False
        counterexample = f"Mean depth {mean_depth} exceeds expected bound by more than 3 standard deviations"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "DPLL_tree_depth",
        "metric_value": mean_depth,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_depth = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_depth) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")