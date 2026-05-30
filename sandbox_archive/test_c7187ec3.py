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
        clauses = set()
        for _ in range(k * n):
            clause = []
            while len(clause) < 2 or any(lit == -other_lit for lit, other_lit in zip(clause, clause[1:])):
                lit = random.randint(1, n)
                if random.choice([True, False]):
                    lit = -lit
                clause.append(lit)
            clauses.add(tuple(sorted(clause)))
        return list(clauses)

    def tropicalize_cnf(cnf):
        support = set()
        for clause in cnf:
            for lit in clause:
                support.add(abs(lit))
        return len(support)

    def resolution_width(cnf):
        # Simplified DPLL solver to estimate resolution width
        clauses = [set(clause) for clause in cnf]
        unit_clauses = {i: set() for i in range(1, 2 * n + 1)}
        for clause in clauses:
            for lit in clause:
                unit_clauses[abs(lit)].add(lit)
        
        def dpll(sat_assignment):
            if not any(clause for clause in clauses if all(lit not in sat_assignment and -lit not in sat_assignment for lit in clause)):
                return True
            literal = next(lit for lit in range(1, 2 * n + 1) if lit not in sat_assignment and -lit not in sat_assignment)
            if dpll(sat_assignment | {literal}):
                return True
            if dpll(sat_assignment | {-literal}):
                return True
            return False
        
        width = 0
        for _ in range(2 * n):
            new_clause = set()
            for lit, unit_clauses_set in unit_clauses.items():
                if len(unit_clauses_set) == 1:
                    new_clause.add(next(iter(unit_clauses_set)))
                    unit_clauses[lit] = set()
            if not new_clause:
                break
            width += 1
        return width

    n_values = [10, 20, 30, 40]
    alpha_values = [0.1, 0.3, 0.5]
    results = []
    
    for n in n_values:
        for _ in range(7):  # Aim for at least 30 instances per seed
            cnf = generate_k_cnf(n, k=3)
            h_min = tropicalize_cnf(cnf)
            t_star = resolution_width(cnf)
            results.append((h_min, math.log2(t_star)))
    
    if len(results) < 12:
        return {
            "metric_name": "Spearman rank correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances"
        }
    
    h_min_values = [h for h, _ in results]
    t_star_log2_values = [math.log2(t) for _, t in results]
    
    def rank(x):
        return sum(1 + sum(1 for y in x if y > z) for z in x)
    
    h_rank = rank(h_min_values)
    t_star_rank = rank(t_star_log2_values)
    
    n_ranks = len(h_min_values)
    spearman_corr = 1 - (6 * sum((h_rank[i] - t_star_rank[i]) ** 2 for i in range(n_ranks))) / (n_ranks * (n_ranks**2 - 1))
    
    return {
        "metric_name": "Spearman rank correlation",
        "metric_value": spearman_corr,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": spearman_corr > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Spearman rank correlation < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")