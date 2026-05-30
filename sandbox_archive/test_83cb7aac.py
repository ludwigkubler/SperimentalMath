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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            while len(set(clause)) < 3:
                clause[random.randint(0, 2)] *= -1
            clauses.append(clause)
        return clauses
    
    def tseitin_tensor_product(cnf1, cnf2):
        n = len(cnf1[0])
        m = len(cnf2[0])
        new_vars = [n + i for i in range(m)]
        new_clauses = []
        
        # Convert CNF to Tseitin encoding
        tseitin_clauses = []
        for clause in cnf1:
            tseitin_clauses.append([i for i in clause if i > 0] + [-new_vars[i - n - 1]])
        for clause in cnf2:
            tseitin_clauses.append([i for i in clause if i > 0] + [-new_vars[n + i - 1]])
        
        # Tseytin tensor product
        for i, clause1 in enumerate(tseitin_clauses):
            for j, clause2 in enumerate(tseitin_clauses):
                new_clause = []
                for lit in clause1:
                    if lit > 0:
                        new_clause.append(lit)
                    else:
                        new_clause.append(-new_vars[i * m + abs(lit) - 1])
                for lit in clause2:
                    if lit > 0:
                        new_clause.append(lit)
                    else:
                        new_clause.append(-new_vars[j * m + abs(lit) - 1])
                new_clauses.append(new_clause)
        
        return new_clauses
    
    def coxeter_group_elements(n):
        # Simplest non-trivial Coxeter group: S_n
        elements = []
        for perm in itertools.permutations(range(1, n + 1)):
            elements.append(perm)
        return elements
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf1 = generate_3cnf(n)
        cnf2 = generate_3cnf(n)
        tensor_product = tseitin_tensor_product(cnf1, cnf2)
        elements = coxeter_group_elements(n)
        
        if len(elements) > 10**6:  # Arbitrary large number to avoid timeout
            return {
                "metric_name": "Coxeter Group Elements",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        results.append(len(elements))
    
    if len(results) < 30:
        return {
            "metric_name": "Coxeter Group Elements",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_samples"
        }
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    conjecture_holds = all(x <= n**2 * math.log(n) for x in results)
    
    return {
        "metric_name": "Coxeter Group Elements",
        "metric_value": mean,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"mean={mean}, std_dev={std_dev}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean={mean_metric_value}, std_dev={std_dev_metric_value}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_samples")