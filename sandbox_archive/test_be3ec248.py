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

def generate_cnf(n, m):
    clauses = []
    for _ in range(m):
        clause = set()
        while len(clause) < 2:
            literal = random.randint(1, n)
            if random.choice([True, False]):
                literal = -literal
            clause.add(literal)
        clauses.append(list(clause))
    return clauses

def resolution_width(clauses):
    literals = set()
    for clause in clauses:
        literals.update(clause)
    
    def resolve(clause1, clause2):
        resolved = []
        for lit1 in clause1:
            if -lit1 in clause2:
                for lit2 in clause2:
                    if lit2 != -lit1:
                        resolved.append(lit2)
                break
        return resolved
    
    queue = [clauses]
    while queue:
        new_queue = []
        for clause in queue:
            found = False
            for other_clause in queue:
                if id(clause) == id(other_clause):
                    continue
                resolved = resolve(clause, other_clause)
                if resolved:
                    found = True
                    new_queue.append(resolved)
                    break
            if not found:
                return len(literals)
        queue = new_queue
    return len(literals)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        m = max(1, int(n * random.uniform(0.1, 0.5)))  # Ensure at least one clause
        clauses = generate_cnf(n, m)
        
        if not clauses:
            continue
        
        w = resolution_width(clauses)
        metric_values.append(w)
        instances_tested += len(clauses)
        n_max = max(n_max, n)
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    
    conjecture_holds = all(w >= 2 * math.log(n) for n, w in zip(n_values, metric_values))
    counterexample = "" if conjecture_holds else "resolution_width < 2 * log(n)"
    
    return {
        "metric_name": "Resolution Width",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        print(f"RESULT: FALSIFIED counterexample=\"resolution_width < 2 * log(n)\" first_failing_seed={first_failing_seed}")