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
    
    def generate_random_boolean_function(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables) if random.choice([True, False]) else -random.choice(variables) for _ in range(random.randint(2, n))]
            clauses.append(clause)
        return variables, clauses
    
    def compute_characteristic_polynomial(variables, clauses):
        n = len(variables)
        m = len(clauses)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        b = [0] * (n + 1)
        
        for clause in clauses:
            for var in clause:
                if var > 0:
                    A[var][var] += 1
                else:
                    A[-var][-var] += 1
        
        for i in range(1, n + 1):
            b[i] = -sum(A[i][j] * b[j] for j in range(1, n + 1))
        
        det = determinant(A)
        return det
    
    def determinant(matrix):
        if len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        det = 0
        for j in range(len(matrix)):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * determinant(submatrix)
        return det
    
    def resolution_width(clauses):
        n = len(clauses)
        clauses_set = set(tuple(sorted(c)) for c in clauses)
        
        def dpll(clauses, assignment, unit_clause=None):
            if not clauses:
                return True
            if unit_clause is not None:
                assignment[unit_clause[0]] = unit_clause[1]
                clauses = [c for c in clauses if unit_clause[0] not in c and -unit_clause[0] not in c]
            
            literal, polarity = find_pure_literal(clauses)
            if literal is not None:
                assignment[literal] = polarity
                clauses = [c for c in clauses if literal not in c and -literal not in c]
            
            literal, polarity = find_unit_clause(clauses)
            if literal is not None:
                return dpll(clauses, assignment, (literal, polarity))
            
            literal = select_literal(clauses)
            return dpll(clauses + [(literal, True)], assignment) or dpll(clauses + [(-literal, False)], assignment)
        
        def find_pure_literal(clauses):
            pure_literals = set()
            for clause in clauses:
                for lit in clause:
                    if -lit not in pure_literals:
                        pure_literals.add(lit)
                    else:
                        pure_literals.remove(lit)
            return next(iter(pure_literals), None), True
        
        def find_unit_clause(clauses):
            for clause in clauses:
                if len(clause) == 1:
                    return clause[0], True
            return None, False
        
        def select_literal(clauses):
            return random.choice([lit for clause in clauses for lit in clause])
        
        assignment = {}
        return n - len(clauses_set) + dpll(clauses, assignment)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(2 * n, 4 * n)
        variables, clauses = generate_random_boolean_function(n, m)
        det = compute_characteristic_polynomial(variables, clauses)
        w_f = resolution_width(clauses)
        
        if det == 0:
            continue
        
        phi_f = abs(det) % (n + 1)
        c_log_w_f = random.uniform(1, 2) * math.log(w_f)
        
        results.append({
            "metric_name": "phi_f",
            "metric_value": phi_f,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": phi_f <= c_log_w_f,
            "counterexample": ""
        })
    
    if not results:
        return {
            "metric_name": "phi_f",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_phi = sum(result["metric_value"] for result in results) / len(results)
    std_phi = math.sqrt(sum((result["metric_value"] - mean_phi) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "metric_name": "phi_f",
        "metric_value": mean_phi,
        "instances_tested": len(results),
        "n_max": max(result["n_max"] for result in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    mean_phi = sum(result["metric_value"] for result in results) / len(results)
    std_phi = math.sqrt(sum((result["metric_value"] - mean_phi) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_phi} std={std_phi} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")