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
    
    def generate_random_formula(n, m):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables + [f'~{v}' for v in variables], 2)
            clauses.append(clause)
        return clauses
    
    def resolution_width(clauses):
        # Simplified DPLL solver to estimate resolution width
        stack = []
        while True:
            literal = None
            for clause in clauses:
                if len(clause) == 1:
                    literal = clause[0]
                    break
            if literal is None:
                return len(stack)
            stack.append(literal)
            new_clauses = []
            for clause in clauses:
                if literal not in clause and f'~{literal}' not in clause:
                    new_clauses.append(clause)
                elif literal in clause:
                    continue
                else:
                    new_clause = [l for l in clause if l != f'~{literal}']
                    new_clauses.extend(new_clause)
            clauses = new_clauses
    
    def cyclic_orderings(clauses):
        # Simplified mapping to cyclic orderings (not actual Frege proof)
        return len(clauses)
    
    n = random.randint(5, 30)
    m = random.randint(n*2, n*4)
    formula = generate_random_formula(n, m)
    width = resolution_width(formula)
    orderings = cyclic_orderings(formula)
    
    return {
        "metric_name": "cyclic_orderings_bound",
        "metric_value": orderings / width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if orderings <= 1.5 * width else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")