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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k):
            clause = set(random.sample(range(1, n+1), 2))
            if random.choice([True, False]):
                clause = {x for x in clause}
            else:
                clause = {-x for x in clause}
            clauses.append(clause)
        return clauses
    
    def tropicalize_cnf(cnf):
        support = set()
        for clause in cnf:
            for lit in clause:
                if lit > 0:
                    support.add(lit)
                else:
                    support.discard(-lit)
        return len(support)
    
    def resolution_width(cnf):
        # Simplified DPLL algorithm to estimate resolution width
        stack = []
        while True:
            unit_clause = None
            for clause in cnf:
                if len(clause) == 1:
                    unit_clause = clause[0]
                    break
            if not unit_clause:
                return len(stack)
            stack.append(unit_clause)
            new_clauses = []
            for clause in cnf:
                if unit_clause in clause:
                    continue
                if -unit_clause in clause:
                    clause.remove(-unit_clause)
                    if not clause:
                        return len(stack)
                else:
                    new_clauses.append(clause)
            cnf = new_clauses
    
    def hodge_index(support):
        return len(support)
    
    n_values = [10, 20, 30, 40]
    alpha_values = [0.1, 0.3, 0.5]
    results = []
    
    for n in n_values:
        for _ in range(30):
            cnf = generate_k_cnf(n, int(n * (n - 1) / k))
            f_trop = tropicalize_cnf(cnf)
            t_star_f = resolution_width(cnf)
            H_min_f_trop = hodge_index(f_trop)
            results.append((H_min_f_trop, math.log2(t_star_f)))
    
    if not results:
        return {
            "metric_name": "Spearman rank correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    # Calculate Spearman rank correlation
    n = len(results)
    ranks_H_min = {x: i+1 for i, (H_min, _) in enumerate(sorted(zip(*results)[0]))}
    ranks_log2_t_star_f = {y: i+1 for i, (_, y) in enumerate(sorted(zip(*results)[1]))}
    
    rho_numerator = sum((ranks_H_min[H_min] - ranks_log2_t_star_f[y]) ** 2 for H_min, y in results)
    rho_denominator = n * (n**2 - 1) / 12
    
    rho = 1 - (6 * rho_numerator) / rho_denominator
    return {
        "metric_name": "Spearman rank correlation",
        "metric_value": rho,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": rho > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_rho = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_rho} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Spearman rank correlation < 0.7' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported")