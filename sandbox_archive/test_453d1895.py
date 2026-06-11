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
        for _ in range(2**n - 1):
            clause = [random.randint(-n, n-1) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(n):
            max_row = rank
            for j in range(rank, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            if A[max_row][i] == 0:
                continue
            A[rank], A[max_row] = A[max_row], A[rank]
            for j in range(m):
                if j != rank:
                    factor = A[j][i] / A[rank][i]
                    for k in range(n):
                        A[j][k] -= factor * A[rank][k]
            rank += 1
        return rank
    
    def diophantine_representation_length(clauses, n):
        variables = set()
        for clause in clauses:
            for lit in clause:
                if lit < 0:
                    variables.add(-lit)
                else:
                    variables.add(lit)
        return len(variables)
    
    def dpll_search_tree_width(clauses, n):
        def dpll(clauses, assignment):
            if not clauses:
                return 1
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                lit = unit_clause[0]
                new_assignment = {**assignment, abs(lit): (lit > 0)}
                new_clauses = [c for c in clauses if not any(l in c or -l in c for l in new_assignment)]
                return dpll(new_clauses, new_assignment)
            pure_literal = next((l for l in range(1, n+1) if all(l in c or -l in c for c in clauses)), None)
            if pure_literal is not None:
                new_assignment = {**assignment, pure_literal: True}
                new_clauses = [c for c in clauses if not any(pure_literal in c or -pure_literal in c for c in clauses)]
                return dpll(new_clauses, new_assignment)
            literal = random.choice([l for l in range(1, n+1) if l not in assignment])
            new_assignment_true = {**assignment, literal: True}
            new_assignment_false = {**assignment, literal: False}
            return max(dpll(clauses, new_assignment_true), dpll(clauses, new_assignment_false))
        
        return dpll(clauses, {})
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_length = 0
        total_width = 0
        
        while instances_tested < 30:
            clauses = generate_sat_instance(n)
            length = diophantine_representation_length(clauses, n)
            width = dpll_search_tree_width(clauses, n)
            
            if length > 0 and width > 0:
                results.append((length, width))
                total_length += length
                total_width += width
                instances_tested += 1
        
        if instances_tested < 30:
            return {
                "metric_name": "Correlation Coefficient",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n_values[-1],
                "conjecture_holds": False,
                "counterexample": "insufficient_instances"
            }
    
    mean_length = total_length / len(results)
    mean_width = total_width / len(results)
    
    correlation_coefficient = sum((x - mean_length) * (y - mean_width) for x, y in results) / (len(results) * math.sqrt(sum((x - mean_length)**2 for x, _ in results)) * math.sqrt(sum((y - mean_width)**2 for _, y in results)))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": n_values[-1],
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<{0.8}\" first_failing_seed={first_failing_seed}")