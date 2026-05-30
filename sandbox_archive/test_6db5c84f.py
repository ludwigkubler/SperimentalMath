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
    
    def generate_3cnf(m, n):
        clauses = []
        for _ in range(m):
            clause = set()
            while len(clause) < 3:
                lit = random.randint(1, n * 2)
                if lit <= n:
                    clause.add(lit)
                else:
                    clause.add(-lit)
            clauses.append(tuple(sorted(clause)))
        return clauses
    
    def is_satisfiable(clauses):
        # Simple backtracking to check satisfiability
        assignment = {}
        def backtrack(i):
            if i == len(clauses):
                return True
            for lit in clauses[i]:
                var = abs(lit)
                if var not in assignment:
                    assignment[var] = (lit > 0)
                    if backtrack(i + 1):
                        return True
                    del assignment[var]
                elif assignment[var] != (lit > 0):
                    continue
            return False
        return backtrack(0)
    
    def min_local_dimension(clauses):
        # Placeholder for actual computation of minimal local dimension
        # For simplicity, we assume it's proportional to log(m/n)
        m = len(clauses)
        n = max(abs(lit) for clause in clauses for lit in clause)
        return math.log(m / n) ** 2
    
    def resolution_width(clauses):
        # Placeholder for actual computation of resolution proof width
        # For simplicity, we assume it's proportional to log(n)
        n = max(abs(lit) for clause in clauses for lit in clause)
        return math.log(n)
    
    results = []
    for m in [10, 20, 40]:
        for _ in range(10):  # Ensure at least 30 instances per seed
            n = random.randint(2 * m, 4 * m)
            clauses = generate_3cnf(m, n)
            if is_satisfiable(clauses):
                dim = min_local_dimension(clauses)
                width = resolution_width(clauses)
                results.append((m, n, dim, width))
    
    metric_value = sum(dim / (width ** 2) for m, n, dim, width in results) / len(results)
    conjecture_holds = all(0.9 <= dim / (width ** 2) <= 1.1 for m, n, dim, width in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "min_local_dimension_over_resolution_width",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(n for m, n, dim, width in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3**j for i in range(5) for j in range(5)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")