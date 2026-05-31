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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for k in range(i+1, n):
                if abs(A[k][i]) > abs(A[max_row][i]):
                    max_row = k
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A
    
    def cnf_to_matrix(clauses):
        n = max(abs(lit) for clause in clauses for lit in clause)
        A = [[0] * (n + 1) for _ in range(len(clauses))]
        for i, clause in enumerate(clauses):
            for lit in clause:
                row = i
                col = abs(lit)
                if lit > 0:
                    A[row][col] = Fraction(1)
                else:
                    A[row][col] = Fraction(-1)
        return A
    
    def dpll(clause_set, assignment, clauses):
        if not clause_set:
            return True
        literal = next(lit for lit in range(1, len(assignment) + 1) if assignment[lit - 1] is None)
        positive_literal = literal
        negative_literal = -literal
        
        def propagate(lit):
            for i, clause in enumerate(clauses):
                if lit in clause:
                    clauses[i].remove(lit)
                    if not clauses[i]:
                        return False
                elif -lit in clause:
                    clauses[i] = [l for l in clause if l != -lit]
            assignment[lit - 1] = True
            return True
        
        if propagate(positive_literal):
            if dpll(clause_set, assignment, clauses):
                return True
            assignment[positive_literal - 1] = None
        if propagate(negative_literal):
            if dpll(clause_set, assignment, clauses):
                return True
            assignment[negative_literal - 1] = None
        
        return False
    
    def generate_cnf(n):
        clauses = []
        for i in range(1, n + 1):
            clause = [random.choice([-i, i]) for _ in range(random.randint(2, 3))]
            clauses.append(clause)
        return clauses
    
    n_max = 40
    instances_tested = 0
    misl_values = []
    dpll_path_lengths = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            clauses = generate_cnf(n)
            A = cnf_to_matrix(clauses)
            rank = sum(1 for row in gaussian_elimination(A) if any(row))
            misl_values.append(rank)
            
            assignment = [None] * n
            clause_set = set(range(len(clauses)))
            dpll_path_length = 0
            while clause_set:
                literal = next(lit for lit in range(1, n + 1) if assignment[lit - 1] is None)
                positive_literal = literal
                negative_literal = -literal
                
                def propagate(lit):
                    nonlocal dpll_path_length
                    for i, clause in enumerate(clauses):
                        if lit in clause:
                            clauses[i].remove(lit)
                            if not clauses[i]:
                                return False
                        elif -lit in clause:
                            clauses[i] = [l for l in clause if l != -lit]
                    assignment[lit - 1] = True
                    dpll_path_length += 1
                    return True
                
                if propagate(positive_literal):
                    if not dpll(clause_set, assignment, clauses):
                        assignment[positive_literal - 1] = None
                else:
                    if propagate(negative_literal):
                        if not dpll(clause_set, assignment, clauses):
                            assignment[negative_literal - 1] = None
        
        instances_tested += 30
    
    misl_mean = sum(misl_values) / len(misl_values)
    dpll_path_length_mean = sum(dpll_path_lengths) / len(dpll_path_lengths)
    
    correlation_coefficient = sum((misl - misl_mean) * (dpll - dpll_path_length_mean) for misl, dpll in zip(misl_values, dpll_path_lengths)) / (len(misl_values) * sum((misl - misl_mean) ** 2 for misl in misl_values) ** 0.5 * sum((dpll - dpll_path_length_mean) ** 2 for dpll in dpll_path_lengths) ** 0.5)
    
    conjecture_holds = correlation_coefficient >= 0.8
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3**j + 5**k for i in range(4) for j in range(4) for k in range(4)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")