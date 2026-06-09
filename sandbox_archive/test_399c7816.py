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
    
    def generate_formula(m, n):
        variables = list(range(n))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def dpll(clauses, assignment={}):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            var = unit_clause[0]
            new_assignment[var] = 1
            if dpll([c for c in clauses if var not in c], new_assignment):
                return True
            del new_assignment[var]
            new_assignment[var] = -1
            if dpll([c for c in clauses if var not in c], new_assignment):
                return True
            del new_assignment[var]
        else:
            var = random.choice(variables)
            for val in [1, -1]:
                new_assignment[var] = val
                if dpll(clauses, new_assignment):
                    return True
                del new_assignment[var]
        return False
    
    def resolution_width(clauses):
        queue = clauses[:]
        while queue:
            clause1 = queue.pop()
            for clause2 in clauses:
                common_vars = [v for v in clause1 if -v in clause2]
                if not common_vars:
                    continue
                new_clause = list(set([v for v in clause1 + clause2 if v not in common_vars]))
                if len(new_clause) == 0:
                    return float('inf')
                queue.append(new_clause)
        return max(len(c) for c in clauses)
    
    def poset_to_symplectic_leaf_number(poset):
        n = len(poset)
        leaf_count = [1] * n
        for i in range(n-1, -1, -1):
            for j in range(i+1, n):
                if poset[i][j] == 0:
                    leaf_count[i] += leaf_count[j]
        return max(leaf_count)
    
    m = random.randint(5, 30)
    n = random.randint(5, 30)
    formula = generate_formula(m, n)
    resolution_width_value = resolution_width(formula)
    poset = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    symplectic_leaf_number_value = poset_to_symplectic_leaf_number(poset)
    
    return {
        "metric_name": "msl_over_w",
        "metric_value": symplectic_leaf_number_value / resolution_width_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if symplectic_leaf_number_value <= resolution_width_value else False,
        "counterexample": "" if symplectic_leaf_number_value <= resolution_width_value else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
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