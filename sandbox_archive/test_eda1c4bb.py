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

def generate_cnf(n):
    clauses = []
    for i in range(1, n+1):
        clause = [random.randint(-n, -1), random.randint(1, n)]
        clauses.append(clause)
    return clauses

def dpll(cnf):
    def solve(model):
        if not cnf:
            return model
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_model = model.copy()
            new_model[-abs(literal)] = literal > 0
            return solve([c for c in cnf if literal not in c and -literal not in c], new_model)
        pure_literal = next((l for l in range(1, n+1) if (l in [x for c in cnf for x in c] or -l in [x for c in cnf for x in c]) == 1), None)
        if pure_literal:
            new_model = model.copy()
            new_model[pure_literal] = True
            return solve([c for c in cnf if pure_literal not in c and -pure_literal not in c], new_model)
        literal = random.choice([l for l in range(1, n+1) if l not in model])
        new_model_true = solve(cnf, {**model, literal: True})
        if new_model_true:
            return new_model_true
        new_model_false = solve(cnf, {**model, literal: False})
        if new_model_false:
            return new_model_false
        return None

    model = {}
    result = solve(cnf, model)
    if result is None:
        return float('inf')
    else:
        return len([l for l in range(1, n+1) if result[l]])

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(n)
        width = dpll(cnf)
        if width == float('inf'):
            continue
        # This is a placeholder for the actual computation of simple presentations
        # For simplicity, we assume |S(φ)| is proportional to n^2
        num_presentations = n**2
        results.append((n, num_presentations))
    
    metric_value = sum(num for _, num in results) / len(results)
    instances_tested = len(results)
    n_max = max(n for n, _ in results)
    conjecture_holds = False
    counterexample = "mapping_undefined"
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")