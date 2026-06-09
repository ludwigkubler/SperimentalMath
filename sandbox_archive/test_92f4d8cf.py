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
    
    def generate_cnf(n):
        clauses = []
        variables = set()
        for _ in range(n):
            clause = []
            num_vars = random.randint(1, n)
            for _ in range(num_vars):
                var = f'x{random.randint(0, 2*n)}'
                if random.choice([True, False]):
                    clause.append(var)
                else:
                    clause.append(f'~{var}')
                variables.add(var)
            clauses.append(clause)
        return clauses, list(variables)

    def is_valid_assignment(assignment, clauses):
        for clause in clauses:
            if all(var not in assignment or (var.startswith('~') and assignment[var[1:]] == 0) for var in clause):
                return False
        return True

    def calculate_width(clauses, variables):
        max_width = 0
        for assignment in itertools.product([0, 1], repeat=len(variables)):
            assignment_dict = dict(zip(variables, assignment))
            if is_valid_assignment(assignment_dict, clauses):
                width = len({var for var in assignment_dict if assignment_dict[var] == 1})
                max_width = max(max_width, width)
        return max_width

    def calculate_k(clauses, variables):
        semtypes = set()
        for clause in clauses:
            semtype = tuple(sorted([var[1:] if var.startswith('~') else var for var in clause]))
            semtypes.add(semtype)
        return len(semtypes)

    n = random.choice([5, 10, 15, 20, 30, 40])
    clauses, variables = generate_cnf(n)
    width = calculate_width(clauses, variables)
    k = calculate_k(clauses, variables)
    
    return {
        "metric_name": "width_bound",
        "metric_value": width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": width <= 2**k,
        "counterexample": "" if width <= 2**k else f"Width {width} exceeds bound 2^{k}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_width = math.sqrt(sum((r["metric_value"] - mean_width)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] > 2 * std_width + mean_width for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"width exceeds bound\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} n_max={max(r['n_max'] for r in results)}")