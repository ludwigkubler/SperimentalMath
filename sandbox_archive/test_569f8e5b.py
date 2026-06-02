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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random

def generate_cnf(n):
    cnf = []
    for _ in range(2 * n):
        clause = [random.randint(-1, -n), random.randint(1, n)]
        if len(set(clause)) == 2:
            cnf.append(clause)
    return cnf

def tseitin_polynomial(cnf, n):
    literals = list(range(1, n + 1))
    for i in range(n):
        literals.append(f"p{i}")
    
    # Create a mapping from literal to variable
    literal_to_var = {l: f"x{l}" for l in literals}
    
    # Initialize the Tseitin polynomial
    tseitin_poly = []
    
    # Add clauses to represent each clause in CNF
    for i, clause in enumerate(cnf):
        var_i = f"p{i}"
        tseitin_poly.append(f"{var_i} <=> ({' v '.join(literal_to_var[l] for l in clause)})")
    
    # Add clauses to ensure the Tseitin variables are consistent
    for i in range(n):
        tseitin_poly.append(f"p{i} <=> (x{i} v ~x{i})")
    
    return tseitin_poly

def resolution_width(cnf):
    # This is a simplified version of resolution width calculation
    # For simplicity, we assume the width is the number of literals in the largest clause
    max_clause_length = max(len(clause) for clause in cnf)
    return max_clause_length

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        tseitin_poly = tseitin_polynomial(cnf, n)
        width = resolution_width(cnf)
        
        # Count the number of maximal ideals (simplified as the number of clauses)
        num_maximal_ideals = len(cnf)
        
        results.append({
            "n": n,
            "num_maximal_ideals": num_maximal_ideals,
            "width": width
        })
    
    # Check if the conjecture holds for all instances
    conjecture_holds = all(result["num_maximal_ideals"] <= result["width"] for result in results)
    counterexample = "" if conjecture_holds else f"n={results[0]['n']}, num_maximal_ideals={results[0]['num_maximal_ideals']}, width={results[0]['width']}"
    
    return {
        "metric_name": "resolution_width",
        "metric_value": sum(result["width"] for result in results) / len(results),
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
    
    # Compute mean/std of metric_value, fraction of seeds where conjecture_holds
    total_metric_value = sum(result["metric_value"] for result in results)
    total_instances_tested = sum(result["instances_tested"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction=1.0")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n']}, num_maximal_ideals={results[0]['num_maximal_ideals']}, width={results[0]['width']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")