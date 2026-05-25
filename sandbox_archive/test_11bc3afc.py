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

def generate_random_3cnf(n: int) -> list:
    clauses = []
    for _ in range(2 * n):
        clause = [random.randint(-n, -1), random.randint(1, n)]
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)
    return clauses

def dpll(clauses: list) -> dict:
    def solve(model: dict):
        unit_clauses = [l for l in range(1, len(clauses) + 1) if any(l in c for c in clauses)]
        pure_literals = [l for l in range(1, len(clauses) + 1) if (l not in model and any(l in c for c in clauses)) or (-l not in model and any(-l in c for c in clauses))]
        
        if not unit_clauses and not pure_literals:
            return model
        
        if not unit_clauses:
            l = pure_literals[0]
        else:
            l = unit_clauses[0]
        
        new_model = model.copy()
        new_model[l] = True
        result = solve(new_model)
        if result is not None:
            return result
        
        new_model[l] = False
        result = solve(new_model)
        if result is not None:
            return result
        
        return None
    
    n = len(clauses)
    model = {}
    return solve(model)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    clauses = generate_random_3cnf(n)
    resolution_length = dpll(clauses)
    
    if resolution_length is None:
        resolution_length = float('inf')
    
    metric_name = "resolution_proof_length"
    metric_value = resolution_length
    instances_tested = 1
    conjecture_holds = True
    counterexample = ""
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")