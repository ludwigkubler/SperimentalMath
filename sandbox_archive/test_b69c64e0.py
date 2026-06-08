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
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf):
        def solve(model):
            if not cnf:
                return True
            literal = next((l for l in model if l != 0), None)
            if literal is None:
                return False
            new_model = model[:]
            new_model[abs(literal) - 1] = literal
            if solve(new_model):
                return True
            new_model[abs(literal) - 1] = -literal
            return solve(new_model)
        return len(cnf) if solve([0] * n) else float('inf')
    
    def algebro_geometric_invariant(cnf):
        # Placeholder for the actual computation of the invariant
        # This is a dummy implementation for demonstration purposes
        return sum(len(clause) for clause in cnf)
    
    n = 15
    instances_tested = 30
    total_r = 0
    total_d = 0
    
    for _ in range(instances_tested):
        cnf = generate_cnf(n)
        r = algebro_geometric_invariant(cnf)
        d = dpll(cnf)
        if d == float('inf'):
            continue
        total_r += math.log(r) if r > 0 else 0
        total_d += d
    
    mean_r = total_r / instances_tested
    mean_d = total_d / instances_tested
    correlation_coefficient = (instances_tested * total_r * total_d - total_r * total_d) / (
        math.sqrt(instances_tested * sum((math.log(r) if r > 0 else 0) ** 2 for r in range(1, n + 1)) - mean_r**2) *
        math.sqrt(instances_tested * sum(d**2 for d in range(1, n + 1)) - mean_d**2))
    
    conjecture_holds = correlation_coefficient >= 0.8 and abs(mean_r - mean_d) <= 3
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n,
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
    
    mean_r = sum(r["metric_value"] for r in results) / len(results)
    std_r = math.sqrt(sum((r["metric_value"] - mean_r)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")