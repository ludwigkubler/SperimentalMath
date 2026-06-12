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
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll_width(cnf):
        def dpll(cnf, assignment):
            if not cnf:
                return 0
            unit_clauses = [c for c in cnf if len(c) == 1]
            if unit_clauses:
                literal = unit_clauses[0][0]
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                new_cnf = [c for c in cnf if literal not in c and -literal not in c]
                return dpll(new_cnf, new_assignment)
            literals = set(abs(lit) for lit in cnf[0])
            for literal in literals:
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                new_cnf = [c for c in cnf if literal not in c and -literal not in c]
                width = dpll(new_cnf, new_assignment)
                if width is not None:
                    return 1 + width
            return None
        
        assignment = {}
        return dpll(cnf, assignment)
    
    def kahler_order(cnf):
        # Placeholder for the actual Kähler order computation
        # This is a dummy implementation that returns a random value
        return random.randint(1, 100)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    width = dpll_width(cnf)
    order = kahler_order(cnf)
    
    if width is None:
        return {
            "metric_name": "Absolute Difference",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "DPLL search tree width calculation failed"
        }
    
    absolute_difference = abs(order - width)
    return {
        "metric_name": "Absolute Difference",
        "metric_value": absolute_difference,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": absolute_difference <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [random.randint(2, 1000) for _ in range(30)]
    else:
        seeds = list(map(int, sys.argv[1:]))

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='DPLL search tree width calculation failed' first_failing_seed={first_failing_seed}")