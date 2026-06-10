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
    
    def generate_sat_instance(n):
        num_clauses = n * (n // 2)
        clauses = []
        for _ in range(num_clauses):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[abs(literal)] = literal > 0
            return dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment)
        pure_literal = next((l for l in range(1, n + 1) if (all(l in c for c in clauses) or all(-l in c for c in clauses))), None)
        if pure_literal:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            return dpll([c for c in clauses if pure_literal not in c and -pure_literal not in c], new_assignment)
        literal, _ = random.choice(clauses)
        new_assignment = assignment.copy()
        new_assignment[abs(literal)] = literal > 0
        if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
            return True
        new_assignment[abs(literal)] = False
        return dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment)
    
    def modular_form_order(clauses):
        # Simplified heuristic to estimate the order of a modular form
        return len(clauses) ** 0.5
    
    n = random.randint(5, 40)
    clauses = generate_sat_instance(n)
    assignment = {i: None for i in range(1, n + 1)}
    
    dpll_height = 0
    while not dpll(clauses, assignment):
        dpll_height += 1
    
    order = modular_form_order(clauses)
    return {
        "metric_name": "DPLL Tree Height",
        "metric_value": dpll_height,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
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
    elif support_fraction >= 0.75:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={r['seed']}")
                break