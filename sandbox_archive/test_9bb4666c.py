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
    
    def generate_truth_table(n):
        return [[random.choice([0, 1]) for _ in range(2**n)] for _ in range(2**n)]
    
    def truth_table_to_cnf(truth_table):
        n = len(truth_table) ** 0.5
        if not n.is_integer():
            raise ValueError("Invalid truth table size")
        n = int(n)
        
        cnf = []
        for i in range(2**n):
            row = truth_table[i]
            if sum(row) == 0:
                continue
            literals = [f"v{i}" if val else f"-v{i}" for i, val in enumerate(row)]
            clause = " & ".join(literals)
            cnf.append(clause)
        return cnf
    
    def resolution_proof_width(cnf):
        clauses = [set(clause.split(" & ")) for clause in cnf]
        
        def resolve(clause1, clause2):
            common_literals = set.intersection(clause1, clause2)
            if len(common_literals) != 2:
                return None
            new_clause = set.union(clause1, clause2) - common_literals
            return " & ".join(sorted(new_clause))
        
        resolved_clauses = set()
        while True:
            new_resolved_clauses = set()
            for i in range(len(resolved_clauses)):
                for j in range(i + 1, len(resolved_clauses)):
                    resolved = resolve(resolved_clauses[i], resolved_clauses[j])
                    if resolved is not None and resolved not in resolved_clauses:
                        new_resolved_clauses.add(resolved)
            if not new_resolved_clauses:
                break
            resolved_clauses.update(new_resolved_clauses)
        
        return len(resolved_clauses)
    
    def minimal_representation_size(truth_table):
        n = len(truth_table) ** 0.5
        if not n.is_integer():
            raise ValueError("Invalid truth table size")
        n = int(n)
        
        # Simplified representation for demonstration purposes
        return n
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        truth_table = generate_truth_table(n)
        width = resolution_proof_width(truth_table)
        M_f = minimal_representation_size(truth_table)
        
        if width is None or M_f is None:
            return {
                "metric_name": "resolution_proof_width",
                "metric_value": None,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        results.append((width, M_f))
    
    if len(results) < 30:
        return {
            "metric_name": "resolution_proof_width",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    widths = [r[0] for r in results]
    M_fs = [r[1] for r in results]
    
    def spearman_rank_correlation(x, y):
        x_ranks = {x[i]: i + 1 for i in range(len(x))}
        y_ranks = {y[i]: i + 1 for i in range(len(y))}
        n = len(x)
        sum_diff_squares = sum((x_ranks[x[i]] - y_ranks[y[i]]) ** 2 for i in range(n))
        return 1 - (6 * sum_diff_squares) / (n * (n**2 - 1))
    
    rho = spearman_rank_correlation(widths, M_fs)
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": rho,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(rho) >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_rho = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_rho} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "resolution_proof_width"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")