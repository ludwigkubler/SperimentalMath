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
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses

    def dpll_solve(clauses):
        def solve(literals, assignment):
            if not literals:
                return True
            literal = literals[0]
            pos_var = abs(literal)
            neg_var = -pos_var
            if pos_var in assignment and assignment[pos_var] != (literal > 0):
                return False
            if neg_var in assignment and assignment[neg_var] != (literal < 0):
                return False
            new_assignment = assignment.copy()
            new_assignment[pos_var] = literal > 0
            if solve(literals[1:], new_assignment):
                return True
            new_assignment[pos_var] = None
            new_assignment[neg_var] = literal < 0
            if solve(literals[1:], new_assignment):
                return True
            return False
        
        assignment = {}
        literals = [l for clause in clauses for l in clause]
        return solve(literals, assignment)

    def tropical_elliptic_curve_rank(clauses):
        # Simplified mapping to a rank based on the number of variables and clauses
        n = max(abs(var) for var in set([abs(lit) for lit in sum(clauses, [])]))
        m = len(clauses)
        return math.sqrt(n * m)

    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / len(x))
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / len(y))
        return cov_xy / (std_x * std_y)

    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        satisfiability_times = []
        ranks = []
        
        for _ in range(30):
            clauses = generate_sat_instance(n)
            start_time = time.time()
            dpll_solve(clauses)
            end_time = time.time()
            satisfiability_times.append(end_time - start_time)
            ranks.append(tropical_elliptic_curve_rank(clauses))
            
            if time.time() - start_time > 200:
                return {
                    "metric_name": "Pearson correlation",
                    "metric_value": None,
                    "instances_tested": len(satisfiability_times),
                    "conjecture_holds": False,
                    "counterexample": "budget_exceeded"
                }
        
        results.append({
            "n": n,
            "satisfiability_times": satisfiability_times,
            "ranks": ranks
        })
    
    correlation_values = [pearson_correlation(result["satisfiability_times"], result["ranks"]) for result in results]
    mean_corr = sum(correlation_values) / len(correlation_values)
    std_corr = math.sqrt(sum((corr - mean_corr) ** 2 for corr in correlation_values) / len(correlation_values))
    
    if all(0.5 <= corr < 0.8 for corr in correlation_values):
        return {
            "metric_name": "Pearson correlation",
            "metric_value": mean_corr,
            "instances_tested": sum(len(result["satisfiability_times"]) for result in results),
            "conjecture_holds": False,
            "counterexample": "correlation_too_low"
        }
    elif all(0.8 <= corr < 1.0 for corr in correlation_values):
        return {
            "metric_name": "Pearson correlation",
            "metric_value": mean_corr,
            "instances_tested": sum(len(result["satisfiability_times"]) for result in results),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not (0.8 <= pearson_correlation(result["satisfiability_times"], result["ranks"]) < 1.0))
        return {
            "metric_name": "Pearson correlation",
            "metric_value": mean_corr,
            "instances_tested": sum(len(result["satisfiability_times"]) for result in results),
            "conjecture_holds": False,
            "counterexample": f"first_failing_seed={first_failing_seed}"
        }

if __name__ == "__main__":
    import time
    import sys
    
    if len(sys.argv) > 1:
        seeds = [int(seed) for seed in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, min(30, len(primes)))
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")