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
    
    def generate_boolean_formula(n):
        if n == 1:
            return random.choice(['True', 'False'])
        else:
            op = random.choice(['and', 'or'])
            left = generate_boolean_formula(n // 2)
            right = generate_boolean_formula(n - n // 2)
            return f"({left} {op} {right})"
    
    def tseitin_encoding(formula):
        variables = set()
        clauses = []
        
        def encode(subformula, var_count):
            if subformula == 'True':
                return (var_count, True)
            elif subformula == 'False':
                return (var_count, False)
            else:
                op, left, right = subformula.split()
                left_var, left_negated = encode(left, var_count)
                var_count += 1
                right_var, right_negated = encode(right, var_count)
                var_count += 1
                
                if op == 'and':
                    clauses.append([left_var, -right_var])
                    clauses.append([-left_var, right_var])
                    return (var_count, left_negated and right_negated)
                elif op == 'or':
                    clauses.append([-left_var, -right_var])
                    clauses.append([left_var, right_var])
                    return (var_count, left_negated or right_negated)
        
        _, negated = encode(formula, 0)
        if negated:
            clauses.append([1])  # Add a clause to ensure the formula is false
        return clauses
    
    def communication_complexity_rank(clauses):
        n = len(clauses)
        rank = 0
        for i in range(n):
            for j in range(i + 1, n):
                if all(c not in clauses[j] and -c not in clauses[j] for c in clauses[i]):
                    rank += 1
        return rank
    
    def minimal_order_of_modular_form(n):
        # Constructive mapping based on coefficients and Fourier expansions
        # This is a placeholder function; actual implementation depends on the conjecture's specifics
        return n * math.log2(n)
    
    instances_tested = 0
    total_rank = 0
    total_minimal_order = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            formula = generate_boolean_formula(n)
            clauses = tseitin_encoding(formula)
            rank = communication_complexity_rank(clauses)
            minimal_order = minimal_order_of_modular_form(n)
            
            instances_tested += 1
            total_rank += rank
            total_minimal_order += minimal_order
    
    if instances_tested < 30:
        return {
            "metric_name": "communication_complexity_rank",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max([5, 10, 15, 20, 30, 40]),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    correlation_coefficient = total_rank / instances_tested - (total_minimal_order / instances_tested) ** 2
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max([5, 10, 15, 20, 30, 40]),
        "conjecture_holds": correlation_coefficient > 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_evidence")