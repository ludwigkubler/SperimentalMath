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
    
    def generate_tseitin_formula(w):
        variables = list(range(1, w + 2))
        clauses = []
        for i in range(1, w + 1):
            clause = [variables[i], -variables[w + i]]
            clauses.append(clause)
            clauses.append([-variables[i], variables[w + i]])
        return clauses
    
    def is_satisfiable(clauses, assignment):
        for clause in clauses:
            if all([assignment[abs(l) - 1] == l > 0 for l in clause]):
                continue
            if any([assignment[abs(l) - 1] == l < 0 for l in clause]):
                return False
        return True
    
    def quandle_action(assignment):
        # Simplified quandle action based on variable assignments
        return sum(assignment)
    
    n = random.randint(5, 40)
    w = random.randint(1, n)
    clauses = generate_tseitin_formula(w)
    satisfiable_assignments = [tuple(random.choice([True, False]) for _ in range(n)) for _ in range(2**n)]
    satisfiable_assignments = [a for a in satisfiable_assignments if is_satisfiable(clauses, a)]
    
    if not satisfiable_assignments:
        return {
            "metric_name": "minimal_index",
            "metric_value": 0,
            "instances_tested": len(satisfiable_assignments),
            "conjecture_holds": False,
            "counterexample": "no_satisfiable_assignments"
        }
    
    min_index = float('inf')
    for assignment in satisfiable_assignments:
        index = quandle_action(assignment)
        if index < min_index:
            min_index = index
    
    return {
        "metric_name": "minimal_index",
        "metric_value": min_index,
        "instances_tested": len(satisfiable_assignments),
        "conjecture_holds": min_index >= 2**(w / 10),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_satisfiable_assignments_found")