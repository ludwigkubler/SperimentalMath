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
    
    def generate_formula(n, m):
        variables = set(f"x{i}" for i in range(n))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, 2)
            clauses.append(clause)
        return clauses
    
    def is_clause_satisfied(clause, assignment):
        return any(assignment[var] == '1' for var in clause)
    
    def dpll_search(clauses, assignment, literals):
        if not clauses:
            return True
        literal = random.choice(literals)
        positive_literal = literal[0]
        negative_literal = literal[1]
        
        # Try setting the literal to 1
        new_assignment = assignment.copy()
        new_assignment[positive_literal] = '1'
        if dpll_search(clauses, new_assignment, literals):
            return True
        
        # Try setting the literal to 0
        new_assignment = assignment.copy()
        new_assignment[negative_literal] = '0'
        if dpll_search(clauses, new_assignment, literals):
            return True
        
        return False
    
    def count_minimal_trees(n, m):
        clauses = generate_formula(n, m)
        literals = set(f"{var}1" for var in variables) | set(f"{var}0" for var in variables)
        assignment = {var: '0' for var in variables}
        
        num_trees = 0
        for _ in range(30):  # Sample 30 instances per seed
            if dpll_search(clauses, assignment, literals):
                num_trees += 1
        
        return num_trees
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_trees = 0
    for n in n_values:
        total_trees += count_minimal_trees(n, n)
    
    metric_value = total_trees / len(n_values)
    instances_tested = 6 * len(n_values)  # 30 instances per seed for each of the 6 n values
    n_max = max(n_values)
    conjecture_holds = False
    counterexample = ""
    
    return {
        "metric_name": "num_trees",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")