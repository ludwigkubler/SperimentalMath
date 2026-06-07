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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tseitin_formula(f, n):
        literals = list(range(-n, 0)) + list(range(1, n+1))
        clauses = []
        
        # Convert the Boolean function to a CNF formula
        for i in range(n):
            clause = [literals[i]]
            for j in range(i+1, n):
                if f[2**(i+j) - 2**i] == 0:
                    clause.append(-literals[j])
                else:
                    clause.append(literals[j])
            clauses.append(clause)
        
        return clauses
    
    def resolution_prove(clauses):
        clauses = set(tuple(sorted(c)) for c in clauses)
        derived = set()
        
        while True:
            new_clauses = set()
            for c1 in clauses:
                for c2 in clauses:
                    if len(set(c1) & set(c2)) == 1:
                        new_clause = tuple(sorted([x for x in c1 + c2 if x not in set(c1) & set(c2)]))
                        if new_clause not in derived and new_clause not in clauses:
                            new_clauses.add(new_clause)
            if not new_clauses:
                break
            clauses.update(new_clauses)
        
        return len(clauses)
    
    def algebraic_degree(f, n):
        degree = 0
        for i in range(2**n):
            if f[i] == 1:
                degree += sum(1 for j in range(n) if (i & (1 << j)) != 0)
        return degree
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        phi_f = tseitin_formula(f, n)
        d_phi_f = resolution_prove(phi_f)
        delta_f = algebraic_degree(f, n)
        
        results.append({
            "n": n,
            "delta_f": delta_f,
            "d_phi_f": d_phi_f
        })
    
    if len(results) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(r["n"] for r in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    delta_values = [r["delta_f"] for r in results]
    d_phi_values = [r["d_phi_f"] for r in results]
    
    mean_delta = sum(delta_values) / len(delta_values)
    mean_d_phi = sum(d_phi_values) / len(d_phi_values)
    
    covariance = sum((delta_values[i] - mean_delta) * (d_phi_values[i] - mean_d_phi) for i in range(len(results))) / len(results)
    variance_delta = sum((delta_values[i] - mean_delta)**2 for i in range(len(results))) / len(results)
    variance_d_phi = sum((d_phi_values[i] - mean_d_phi)**2 for i in range(len(results))) / len(results)
    
    correlation_coefficient = covariance / (math.sqrt(variance_delta) * math.sqrt(variance_d_phi))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": correlation_coefficient >= 0.7 and all(c >= 0.5 for c in [correlation_coefficient]),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_below_0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")