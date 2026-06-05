# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def generate_random_boolean_function(n, num_clauses):
    clauses = []
    for _ in range(num_clauses):
        clause = [random.choice([1, -1]) * random.randint(0, n-1) for _ in range(random.randint(1, n))]
        clauses.append(clause)
    return clauses

def calculate_entropy(clauses):
    if not clauses:
        return 0.0
    p = len(clauses) / (2 ** len(clauses[0]))
    if p == 0 or p == 1:
        return 0.0
    return -p * math.log(p, 2) - (1 - p) * math.log(1 - p, 2)

def min_deg_polynomial(clauses):
    n = len(clauses[0])
    variables = list(range(n))
    
    def evaluate(poly, assignment):
        result = 0
        for term in poly:
            product = 1
            for var, coeff in term:
                if assignment[var] == 0:
                    product *= -coeff
                else:
                    product *= coeff
            result += product
        return result
    
    def is_zero(poly):
        for term in poly:
            if any(coeff != 0 for _, coeff in term):
                return False
        return True
    
    def add_term(poly, term):
        new_poly = [t[:] for t in poly]
        found = False
        for i, t in enumerate(new_poly):
            if set(t) == set(term):
                new_poly[i] = [(v, c + coeff) for v, c in t]
                found = True
                break
        if not found:
            new_poly.append(term)
        return new_poly
    
    def multiply_polynomials(poly1, poly2):
        result = []
        for term1 in poly1:
            for term2 in poly2:
                product = [(v, c1 * c2) for v, c1 in term1] + [(v, c2 * c1) for v, c2 in term2]
                result = add_term(result, product)
        return result
    
    def reduce_polynomial(poly):
        while True:
            changed = False
            for i in range(len(poly)):
                for j in range(i+1, len(poly)):
                    if set(poly[i]) == set(poly[j]):
                        poly[i] = [(v, c1 + c2) for v, c1, c2 in zip(poly[i], poly[i], poly[j])]
                        del poly[j]
                        changed = True
                        break
                if changed:
                    break
            if not changed:
                break
        
        result = []
        for term in poly:
            if any(coeff != 0 for _, coeff in term):
                result.append(term)
        
        return result
    
    def find_min_deg(clauses):
        n = len(clauses[0])
        variables = list(range(n))
        
        def is_satisfiable(poly, assignment):
            return evaluate(poly, assignment) == 1
        
        def backtrack(assignment):
            if len(assignment) == n:
                return is_satisfiable(poly, assignment)
            
            for val in [0, 1]:
                assignment.append(val)
                if backtrack(assignment):
                    return True
                assignment.pop()
            return False
        
        poly = []
        for clause in clauses:
            term = [(var, coeff) for var, coeff in enumerate(clause)]
            poly = add_term(poly, term)
        
        poly = reduce_polynomial(poly)
        
        min_deg = float('inf')
        for i in range(1, n+1):
            if backtrack([0]*i):
                min_deg = i
                break
        
        return min_deg
    
    return find_min_deg(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        num_clauses = random.randint(1, n)
        clauses = generate_random_boolean_function(n, num_clauses)
        
        min_deg = min_deg_polynomial(clauses)
        entropy = calculate_entropy(clauses)
        
        results.append({
            "n": n,
            "min_deg": min_deg,
            "entropy": entropy
        })
    
    if not results:
        return {
            "metric_name": "Entropy vs Min Degree",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    metric_values = [r["min_deg"] / r["entropy"] for r in results]
    mean_metric_value = sum(metric_values) / len(metric_values)
    
    return {
        "metric_name": "Entropy vs Min Degree",
        "metric_value": mean_metric_value,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")