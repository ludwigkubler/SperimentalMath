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
    
    def generate_tseitin_formula(n):
        variables = list(range(1, n+1))
        clauses = []
        
        # Generate clauses for each variable
        for i in range(1, n+1):
            clause = [f"v{i}"]
            for j in range(i+1, n+1):
                clause.append(f"-v{j}")
            clauses.append(clause)
            
            clause = [-f"v{i}"]
            for j in range(i+1, n+1):
                clause.append(f"v{j}")
            clauses.append(clause)
        
        # Generate clauses for implications
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                clause = [-f"v{i}", f"v{j}"]
                clauses.append(clause)
        
        return clauses
    
    def formal_context_from_clauses(clauses):
        context = {}
        for clause in clauses:
            for var in clause:
                if var[0] == '-':
                    var = var[1:]
                if var not in context:
                    context[var] = set()
                context[var].add(tuple(sorted([v for v in clause if v != var])))
        return context
    
    def minimal_order(context):
        order = 0
        for item in context.values():
            order += len(item)
        return order
    
    def circuit_monotone_width(clauses):
        width = 0
        for clause in clauses:
            width = max(width, len(clause))
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_tseitin_formula(n)
        context = formal_context_from_clauses(cnf)
        order = minimal_order(context)
        width = circuit_monotone_width(cnf)
        
        if order > width ** 0.5:
            return {
                "metric_name": "order_vs_monotone_width",
                "metric_value": order / width,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"n={n}, order={order}, width={width}"
            }
    
    return {
        "metric_name": "order_vs_monotone_width",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100, 2))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = (sum((x - mean) ** 2 for x in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r <= 1) / len(results)
    
    if all(r <= 1 for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = seeds[next(i for i, r in enumerate(results) if r > 1)]
        print(f"RESULT: FALSIFIED counterexample=\"n={first_failing_seed}\" first_failing_seed={first_failing_seed}")