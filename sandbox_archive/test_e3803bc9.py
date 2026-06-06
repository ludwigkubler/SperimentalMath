# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import product, combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tensor_representation(f, n):
        tensor = [[f[i] if j == i else 0 for j in range(2**n)] for i in range(2**n)]
        return tensor
    
    def geometric_entropy(tensor):
        total = sum(tensor[i][j] for i in range(len(tensor)) for j in range(len(tensor[0])))
        entropy = 0
        for i in range(len(tensor)):
            row_sum = sum(tensor[i])
            if row_sum > 0:
                p = Fraction(row_sum, total)
                entropy -= p * math.log2(p)
        return entropy
    
    def circuit_size(f, n):
        # Simplified DPLL algorithm to find the size of the smallest circuit
        def dpll(cnf, assignment):
            if not cnf:
                return True
            unit_clause = next((c for c in cnf if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_assignment = assignment.copy()
                new_assignment[literal] = literal > 0
                if dpll([c for c in cnf if literal not in c], new_assignment):
                    return True
                new_assignment[literal] = not literal > 0
                if dpll([c for c in cnf if -literal not in c], new_assignment):
                    return True
                return False
            pure_literal = next((l for l in range(1, n+1) if (l not in assignment and -l not in assignment)), None)
            if pure_literal:
                new_assignment[pure_literal] = True
                if dpll(cnf, new_assignment):
                    return True
                new_assignment[pure_literal] = False
                if dpll(cnf, new_assignment):
                    return True
                return False
            literal = next((l for l in range(1, n+1) if l not in assignment), None)
            new_assignment[literal] = True
            if dpll([c for c in cnf if literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll(cnf, new_assignment):
                return True
            return False
        
        def cnf_to_clauses(cnf):
            clauses = []
            for clause in cnf:
                if isinstance(clause, list):
                    clauses.append(clause)
                else:
                    clauses.append([clause])
            return clauses
        
        cnf = generate_cnf(f, n)
        if cnf is None:
            return 0
        assignment = {}
        size = 0
        while not dpll(cnf, assignment):
            literal = next((l for l in range(1, n+1) if l not in assignment), None)
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll(cnf, new_assignment):
                assignment[literal] = True
                size += 1
            else:
                new_assignment[literal] = False
                if dpll(cnf, new_assignment):
                    assignment[literal] = False
                    size += 1
        return size
    
    def generate_cnf(f, n):
        # Simplified CNF generation for a random Boolean function
        cnf = []
        for i in range(2**n):
            clause = []
            for j in range(n):
                if f[i] == 0:
                    clause.append(-j-1)
                else:
                    clause.append(j+1)
            cnf.append(clause)
        return cnf
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        tensor = tensor_representation(f, n)
        entropy = geometric_entropy(tensor)
        s_f = circuit_size(f, n)
        if s_f == 0:
            continue
        results.append({"n": n, "entropy": entropy, "s_f": s_f})
    
    if not results:
        return {
            "metric_name": "geometric_entropy",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_entropy = sum(result["entropy"] for result in results) / len(results)
    mean_s_f = sum(result["s_f"] for result in results) / len(results)
    correlation_coefficient = 0
    if mean_s_f != 0:
        correlation_coefficient = sum((result["entropy"] - mean_entropy) * (math.log2(result["s_f"]) - math.log2(mean_s_f)) for result in results) / len(results)
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")