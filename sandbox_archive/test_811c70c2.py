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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def truth_table_to_cnf(truth_table, n):
    cnf = []
    for i in range(2**n):
        row = format(i, f'0{n}b')
        literals = [f"x{i}" if bit == '1' else f"-x{i}" for i, bit in enumerate(row)]
        clause = " & ".join(literals)
        cnf.append(clause)
    return cnf

def resolution_proof_width(cnf):
    clauses = cnf
    while True:
        new_clauses = []
        added_clause = False
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                literals_i = set(clause.split(" & ") for clause in clauses[i].split(" | "))
                literals_j = set(clause.split(" & ") for clause in clauses[j].split(" | "))
                complemented_literals = [lit for lit in literals_i if "-" + lit not in literals_j]
                if len(complemented_literals) == 1:
                    new_clause = " | ".join(lit for lit in literals_i if lit != complemented_literals[0]) + " | " + " | ".join(lit for lit in literals_j if lit != "-" + complemented_literals[0])
                    if new_clause not in new_clauses:
                        new_clauses.append(new_clause)
                        added_clause = True
        if not added_clause:
            return len(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        function = generate_boolean_function(n)
        truth_table = truth_table_to_cnf(function, n)
        width = resolution_proof_width(truth_table)
        M_f = len([clause.split(" & ") for clause in truth_table])
        
        if M_f <= 0 or width <= 0:
            continue
        
        results.append({"n": n, "M_f": M_f, "width": width})
    
    if not results:
        return {
            "metric_name": "resolution_proof_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    M_f_values = [result["M_f"] for result in results]
    width_values = [result["width"] for result in results]
    
    n_max = max(result["n"] for result in results)
    instances_tested = len(results)
    
    # Calculate Spearman's rank correlation coefficient
    def rank(data):
        return {x: i + 1 for i, x in enumerate(sorted(set(data), reverse=True))}
    
    M_f_rank = rank(M_f_values)
    width_rank = rank(width_values)
    
    n = len(M_f_values)
    sum_diff_ranks_squared = sum((M_f_rank[M_f_values[i]] - width_rank[width_values[i]])**2 for i in range(n))
    spearman_corr = 1 - (6 * sum_diff_ranks_squared) / (n * (n**2 - 1))
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": spearman_corr,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(spearman_corr) >= 0.95,  # Threshold for correlation
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, ...run_trial output...}}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    instances_tested = sum(r["instances_tested"] for r in results)
    n_max = max(r["n_max"] for r in results)
    conjecture_holds = all(r["conjecture_holds"] for r in results)
    
    if conjecture_holds:
        mean = sum(metric_values) / len(metric_values)
        std = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")