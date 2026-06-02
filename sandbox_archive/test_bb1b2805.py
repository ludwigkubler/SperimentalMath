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
            clauses.append(clause)
        return clauses
    
    def dpll(cnf):
        assignment = {}
        
        def solve(literals, assignment):
            if not literals:
                return True
            literal = literals[0]
            for value in [True, False]:
                assignment[literal] = value
                if all(any(not (l == -var or l == var) for var in clause) for clause in cnf):
                    if solve(literals[1:], assignment):
                        return True
                del assignment[literal]
            return False
        
        return solve(list(range(1, len(cnf) + 1)), assignment)
    
    def rank_k(cnf):
        # Simplified implementation of computing minimal rank for demonstration purposes
        return len(cnf)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    depth = dpll(cnf)
    rank = rank_k(cnf)
    
    if depth is None:
        return {
            "metric_name": "rank_k",
            "metric_value": float('nan'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "dpll returned None"
        }
    
    correlation_coefficient = (2 * depth - n) / n
    
    return {
        "metric_name": "rank_k",
        "metric_value": correlation_coefficient,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": correlation_coefficient >= 0.7 and rank <= 2 * n**2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if not math.isnan(r["metric_value"])) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results if not math.isnan(r["metric_value"])) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(not math.isnan(r["metric_value"]) and r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not math.isnan(r["metric_value"]) and not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not math.isnan(result["metric_value"]) and not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7 or rank_k > 2n^2\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no valid results found")