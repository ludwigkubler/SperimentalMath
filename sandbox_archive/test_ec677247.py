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
    
    def generate_tseitin_formula(n, num_clauses):
        variables = list(range(1, n + 1))
        clauses = []
        
        for i in range(num_clauses):
            clause = [random.choice(variables)]
            if random.choice([True, False]):
                clause.append(random.choice(variables))
            if random.choice([True, False]):
                clause.append(-random.choice(variables))
            clauses.append(clause)
        
        # Create the Tseitin formula
        tseitin_formula = []
        for i, clause in enumerate(clauses):
            tseitin_var = n + i + 1
            tseitin_formula.append([tseitin_var])
            for var in clause:
                if var > 0:
                    tseitin_formula.append([-tseitin_var, var])
                else:
                    tseitin_formula.append([-tseitin_var, -var])
        
        return tseitin_formula
    
    def resolution_width(formula):
        # Simplify the formula using resolution
        clauses = set(tuple(clause) for clause in formula)
        new_clauses = set()
        
        while True:
            added_clause = False
            for clause1 in clauses:
                for clause2 in clauses:
                    if len(set(clause1).intersection(set(clause2))) == 1:
                        new_clause = tuple(sorted([x for x in clause1 + clause2 if x != -x]))
                        if new_clause not in clauses and new_clause not in new_clauses:
                            new_clauses.add(new_clause)
                            added_clause = True
            if not added_clause:
                break
            clauses.update(new_clauses)
            new_clauses.clear()
        
        return len(clauses)
    
    def smallest_p_adic_exponent(num):
        p = 2
        e = 0
        while num % p == 0:
            num //= p
            e += 1
        return e
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            num_clauses = int(n * (random.random() + 0.1) * 10)
            formula = generate_tseitin_formula(n, num_clauses)
            width = resolution_width(formula)
            e = smallest_p_adic_exponent(num_clauses)
            metric_value = math.log2(p**n / num_clauses)
            
            results.append({
                "metric_name": "resolution_width",
                "metric_value": width,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": abs(width - metric_value) <= 3 * math.log2(p**n / num_clauses),
                "counterexample": ""
            })
    
    return {
        "seed": seed,
        "metric_name": "resolution_width",
        "metric_value": sum(result["metric_value"] for result in results) / len(results),
        "instances_tested": len(results),
        "n_max": max(result["n_max"] for result in results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")