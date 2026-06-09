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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, n))]
            if all(abs(x) != abs(y) for x, y in combinations(clause, 2)):
                clauses.append(clause)
        return clauses
    
    def dpll(cnf):
        def solve(model):
            if not cnf:
                return model
            var = next((v for v in range(1, n+1) if v not in model and -v not in model), None)
            if var is None:
                return model
            pos_model = solve(model | {var: True})
            if pos_model:
                return pos_model
            return solve(model | {var: False})
        return solve({})
    
    def frege_proof_depth(cnf):
        return len(dpll(cnf))
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_folds = 0
    total_depths = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n)
            depth = frege_proof_depth(cnf)
            if depth == 0:
                continue
            total_folds += len(cnf)  # Simplified fold count as number of clauses
            total_depths += depth
            instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": "Folds vs Depth Ratio",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_fold = total_folds / instances_tested
    mean_depth = total_depths / instances_tested
    ratio = mean_fold / mean_depth
    
    return {
        "metric_name": "Folds vs Depth Ratio",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": abs(ratio) <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if abs(r["metric_value"]) <= 1.5) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"ratio_exceeds_bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_evidence")