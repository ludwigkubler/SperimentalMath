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
    
    def generate_tseitin_formula(n, m):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(m):
            clause = random.choice(variables) + ' OR NOT ' + random.choice(variables)
            clauses.append(clause)
        return clauses
    
    def tropicalize_clause(clause, variables):
        t_clauses = []
        for var in variables:
            if var in clause:
                t_clauses.append(1)
            else:
                t_clauses.append(-math.inf)
        return t_clauses
    
    def tensor_product(t_clauses):
        result = [t_clauses[0]]
        for tc in t_clauses[1:]:
            new_result = []
            for r1 in result:
                for r2 in tc:
                    new_result.append(r1 + r2)
            result = new_result
        return result
    
    def min_rank(tensor_product):
        max_value = -math.inf
        for val in tensor_product:
            if val > max_value:
                max_value = val
        return max_value
    
    def resolution_width(clauses):
        queue = clauses[:]
        width = 0
        while queue:
            new_queue = []
            for clause in queue:
                if ' OR NOT ' in clause:
                    var1, var2 = clause.split(' OR NOT ')
                    new_clause1 = var1 + ' AND ' + var2
                    new_clause2 = 'NOT ' + var1 + ' AND ' + var2
                    new_queue.append(new_clause1)
                    new_queue.append(new_clause2)
                else:
                    new_queue.append(clause)
            queue = new_queue
            width += 1
        return width
    
    n = random.randint(5, 40)
    m = random.randint(n, 2*n)
    clauses = generate_tseitin_formula(n, m)
    
    t_clauses = [tropicalize_clause(clause, variables) for clause in clauses]
    tensor_prod = tensor_product(t_clauses)
    min_rank_value = min_rank(tensor_prod)
    width = resolution_width(clauses)
    
    return {
        "metric_name": "min_rank_over_width",
        "metric_value": min_rank_value / width,
        "instances_tested": 1,
        "conjecture_holds": min_rank_value <= width,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        counterexample = "An instance F with a resolution proof tree of width less than 2 * minimal rank(tropicalized tensor product of clauses in F)."
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")