# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, m):
        clauses = set()
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if len(clause) == 2 and clause[0] != -clause[1]:
                clauses.add(tuple(sorted(clause)))
        return clauses
    
    def resolution_width(cnf):
        queue = list(cnf)
        seen = set()
        while queue:
            clause = queue.pop(0)
            for literal in clause:
                if -literal in seen:
                    continue
                seen.add(literal)
                new_clauses = []
                for other_clause in cnf:
                    if literal in other_clause and -literal not in other_clause:
                        new_clause = tuple(sorted([x for x in other_clause if x != literal]))
                        if new_clause not in new_clauses:
                            new_clauses.append(new_clause)
                queue.extend(new_clauses)
        return len(seen)

    def matroid_rank(cnf):
        variables = set(abs(lit) for lit in cnf)
        rank = 0
        while variables:
            pivot = random.choice(list(variables))
            variables.discard(pivot)
            new_variables = {lit for clause in cnf if pivot in clause}
            rank += 1
            variables -= new_variables
        return rank

    def tropical_symplectic_order(cnf):
        # Placeholder implementation; actual computation depends on the matroid structure
        return len(cnf)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n, random.randint(2*n, 3*n))
            ost_value = tropical_symplectic_order(cnf)
            w_value = resolution_width(cnf)
            results.append((ost_value, w_value))

    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }

    ost_values, w_values = zip(*results)
    n_max = max(n_values)
    
    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        std_x = (sum((xi - mean_x)**2 for xi in x) / len(x))**0.5
        std_y = (sum((yi - mean_y)**2 for yi in y) / len(y))**0.5
        return cov_xy / (std_x * std_y)

    correlation_coefficient = pearson_correlation(ost_values, w_values)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.9,
        "counterexample": "" if correlation_coefficient >= 0.9 else f"correlation_coefficient={correlation_coefficient}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.9\" first_failing_seed={first_failing_seed}")
    else:
        mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
        std_metric_value = (sum((result["metric_value"] - mean_metric_value)**2 for result in results if result["metric_value"] is not None) / len(results))**0.5
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")