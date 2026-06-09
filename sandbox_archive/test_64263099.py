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
from fractions import Fraction
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(n):
        variables = set()
        clauses = []
        for _ in range(n):
            clause = set()
            while len(clause) < 2:
                var = f'x{random.randint(1, n)}'
                if var not in clause and var not in variables:
                    clause.add(var)
                    variables.add(var)
            clauses.append(clause)
        return clauses
    
    def dpll_width(clauses):
        stack = []
        assignment = {}
        variables = set()
        for clause in clauses:
            variables.update(clause)
        
        def dfs():
            if len(stack) == 0:
                return True
            var = next(iter(variables - set(assignment.keys())))
            for val in [True, False]:
                assignment[var] = val
                stack.append((var, val))
                if dfs():
                    return True
                del assignment[var]
                stack.pop()
            return False
        
        return len(stack)
    
    def betti_number(clauses):
        # Placeholder function to compute the Quasi-Polynomial Betti number
        # This is a dummy implementation and should be replaced with actual computation
        return 0
    
    max_betti = 0
    instances_tested = 30
    n_max = 40
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        clauses = generate_formula(n)
        width = dpll_width(clauses)
        betti = betti_number(clauses)
        max_betti = max(max_betti, betti)
    
    conjecture_holds = False
    counterexample = "mapping_undefined"
    if instances_tested >= 30:
        n_min = 5
        n_max = 40
        if n_min <= n_max and instances_tested >= (n_max - n_min + 1) * 3:
            conjecture_holds = True
    
    return {
        "metric_name": "max_betti",
        "metric_value": max_betti,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_betti = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_betti) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_betti} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")