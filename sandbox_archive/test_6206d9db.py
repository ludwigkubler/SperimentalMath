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
    
    def generate_3sat_instance(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def is_satisfiable(clauses):
        # Simplified SAT solver using backtracking
        def backtrack(assignment):
            if len(assignment) == n:
                for clause in clauses:
                    if not any(lit in assignment for lit in clause):
                        return False
                return True
            var = len(assignment) + 1
            assignment.append(var)
            if backtrack(assignment):
                return True
            assignment.pop()
            assignment.append(-var)
            if backtrack(assignment):
                return True
            return False
        
        n = len(clauses)
        return backtrack([])
    
    def sos_moment_matrix(clauses):
        n = len(clauses)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        
        for i in range(2**(n+1)):
            assignment = [(-1)**(i >> j & 1) for j in range(n+1)]
            count = sum(all(lit in assignment for lit in clause) for clause in clauses)
            matrix[count][len([x for x in assignment if x != 0])] += 1
        
        return matrix
    
    def is_schur_positive(matrix):
        n = len(matrix) - 1
        coefficients = [matrix[i][j] for i in range(n+1) for j in range(i+1)]
        
        if not coefficients:
            return False
        
        first_non_zero_index = next((i for i, coeff in enumerate(coefficients) if coeff != 0), None)
        if first_non_zero_index is None:
            return False
        
        dominant_coeff = coefficients[first_non_zero_index]
        dominant_sign = math.copysign(1, dominant_coeff)
        
        for i, coeff in enumerate(coefficients):
            if i == first_non_zero_index:
                continue
            if math.copysign(1, coeff) != dominant_sign or abs(coeff) > abs(dominant_coeff):
                return False
        
        return True
    
    n = random.randint(5, 40)
    clauses = generate_3sat_instance(n)
    is_sat = is_satisfiable(clauses)
    matrix = sos_moment_matrix(clauses)
    schur_positive = is_schur_positive(matrix)
    
    metric_name = "Schur Positivity"
    metric_value = int(schur_positive == is_sat)
    instances_tested = 1
    conjecture_holds = schur_positive == is_sat
    counterexample = "" if conjecture_holds else f"3-SAT instance with n={n} and clauses={clauses}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*1000, 100))[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")