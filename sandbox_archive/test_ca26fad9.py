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
    
    def characteristic_polynomial(matrix):
        n = len(matrix)
        if n == 0:
            return [Fraction(1)]
        
        # Gaussian elimination to find the determinant
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            denom = matrix[i][i]
            if denom == 0:
                continue
            
            for j in range(i+1, n):
                factor = matrix[j][i] / denom
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        
        det = Fraction(1)
        for i in range(n):
            det *= matrix[i][i]
        
        return [det]
    
    def resolution_width(clauses, variables):
        # Simplified DPLL solver to estimate width
        clauses = set(tuple(sorted(c)) for c in clauses)
        variables = sorted(variables)
        stack = []
        assignment = {}
        width = 0
        
        def dpll():
            nonlocal width
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                assignment[literal] = literal > 0
                clauses.discard(unit_clause)
                clauses.discard(tuple(-literal,))
                width = max(width, abs(literal))
                return dpll()
            
            literal = next((v for v in variables if v not in assignment), None)
            if literal is None:
                return False
            
            assignment[literal] = True
            stack.append((-literal, assignment.copy()))
            if dpll():
                return True
            
            del assignment[literal]
            literal = -literal
            assignment[literal] = True
            width = max(width, abs(literal))
            if dpll():
                return True
            
            del assignment[literal]
            stack.pop()
            return False
        
        dpll()
        return width
    
    def generate_boolean_function(n):
        variables = list(range(1, n+1))
        clauses = []
        for _ in range(2**n):
            clause = random.sample(variables, k=random.randint(1, n))
            clauses.append(clause)
        return clauses, variables
    
    n = 5
    while n <= 40:
        clauses, variables = generate_boolean_function(n)
        poly = characteristic_polynomial([[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)])
        w_f = resolution_width(clauses, variables)
        
        if w_f == 0:
            continue
        
        phi_f = abs(poly[0])
        c = 2  # Example constant
        bound = c * math.log(w_f)
        
        if phi_f > bound:
            return {
                "metric_name": "phi_f vs c log w(f)",
                "metric_value": phi_f,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"phi_f={phi_f} > {c} * log({w_f}) = {bound}"
            }
        
        n *= 2
    
    return {
        "metric_name": "phi_f vs c log w(f)",
        "metric_value": None,  # Not applicable for this conjecture
        "instances_tested": 0,
        "n_max": 40,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        max_n = max(max(r["n_max"] for r in results), 16)
        if any(not r["conjecture_holds"] for r in results):
            first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
            counterexample = next(r["counterexample"] for r in results if r["conjecture_holds"] == False)
            support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        else:
            counterexample = ""
            support_fraction = 1.0
        
        mean_value, std_dev = None, None
    
    print(f"RESULT: {'SUPPORTED' if all(r['conjecture_holds'] for r in results) else 'FALSIFIED'} mean={mean_value} std={std_dev} support_fraction={support_fraction}")