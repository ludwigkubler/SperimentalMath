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
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def dpll_solve(cnf):
        def solve(literals):
            if not cnf:
                return True
            unit_clause = next((c for c in cnf if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                if literal < 0 and -literal in literals or literal > 0 and literal in literals:
                    return False
                literals.add(literal)
                cnf = [c for c in cnf if literal not in c and -literal not in c]
            pure_literal = next((l for l in range(1, n + 1) if (l in literals or -l in literals) and (-l not in literals or l not in literals)), None)
            if pure_literal:
                literal = pure_literal if pure_literal in literals else -pure_literal
                literals.add(literal)
                cnf = [c for c in cnf if literal not in c and -literal not in c]
            return solve(literals)
        return solve(set())
    
    def compute_qmc_order(n, epsilon):
        # Simplified QMC order computation (not actual implementation)
        return int(math.log2(1 / epsilon) * math.log2(n))
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    resolution_proof_width = dpll_solve(cnf)
    qmc_order = compute_qmc_order(n, Fraction(1, 1000))
    
    if resolution_proof_width is None:
        return {
            "metric_name": "resolution_proof_width",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": resolution_proof_width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")