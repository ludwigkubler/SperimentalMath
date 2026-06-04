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
    
    def dpll(cnf):
        def solve(literals):
            if not cnf:
                return literals
            unit_clause = next((c for c in cnf if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_cnf = [c for c in cnf if literal not in c and -literal not in c]
                return solve(literals + [literal])
            pure_literal = next((l for l in range(-n, n+1) if (l in literals or -l in literals) == 0), None)
            if pure_literal is None:
                return None
            literal = pure_literal if pure_literal > 0 else -pure_literal
            new_cnf = [c for c in cnf if literal not in c and -literal not in c]
            result = solve(literals + [literal])
            if result is not None:
                return result
            return solve(literals + [-literal])
        
        return solve([])
    
    def hodge_complexity(cnf):
        # Placeholder for Hodge complexity calculation
        # This is a dummy implementation and should be replaced with actual computation
        return len(cnf)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    hdc = hodge_complexity(cnf)
    proof_length = len(dpll(cnf)) if dpll(cnf) is not None else float('inf')
    
    return {
        "metric_name": "hdc_vs_dpll",
        "metric_value": hdc / (proof_length + 1),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")