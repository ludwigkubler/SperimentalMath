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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def resolution_width(cnf):
        clauses = set(tuple(sorted(c)) for c in cnf)
        learned_clauses = []
        
        while True:
            new_clause = None
            for c1 in clauses:
                for c2 in learned_clauses:
                    if len(set(c1) & set(c2)) == 1:
                        lit = next(lit for lit in c1 if lit not in c2 and -lit not in c2)
                        new_clause = tuple(sorted([x for x in c1 + c2 if x != lit and -x != lit]))
                        break
                if new_clause:
                    break
            if not new_clause:
                return len(learned_clauses)
            learned_clauses.append(new_clause)
    
    def matroid_rank(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        rank = 0
        elements = set(range(1, n + 1))
        
        while elements:
            independent_set = []
            for element in elements:
                new_set = independent_set + [element]
                if all(all(lit not in c and -lit not in c for c in cnf) for lit in new_set):
                    independent_set.append(element)
            rank += 1
            elements -= set(independent_set)
        
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            cnf = generate_cnf(n, int(1.5 * n))
            ost_L_phi = matroid_rank(cnf)
            w_phi = resolution_width(cnf)
            results.append((ost_L_phi, w_phi))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    ost_values, w_values = zip(*results)
    mean_ost = sum(ost_values) / len(ost_values)
    mean_w = sum(w_values) / len(w_values)
    
    correlation_coefficient = 0
    if len(ost_values) > 1:
        numerator = sum((x - mean_ost) * (y - mean_w) for x, y in zip(ost_values, w_values))
        denominator = math.sqrt(sum((x - mean_ost) ** 2 for x in ost_values)) * math.sqrt(sum((y - mean_w) ** 2 for y in w_values))
        if denominator != 0:
            correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient < 0.9' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_results")