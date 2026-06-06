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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tensor_representation(f, n):
        if n == 1:
            return f
        else:
            half = n // 2
            left_half = tensor_representation(f[:2**(half)], half)
            right_half = tensor_representation(f[2**(half):], half)
            result = []
            for i in range(2**half):
                for j in range(2**half):
                    result.append(left_half[i] * right_half[j])
            return result
    
    def geometric_entropy(tensor, n):
        count = [0] * 2
        for value in tensor:
            count[value] += 1
        entropy = 0
        for c in count:
            if c > 0:
                p = Fraction(c, len(tensor))
                entropy -= p * math.log(p, 2)
        return entropy
    
    def circuit_size(f, n):
        clauses = []
        variables = list(range(1, n+1))
        
        def to_cnf(formula):
            if isinstance(formula, int):
                return formula
            elif formula == 'or':
                return (to_cnf(formula[0]), to_cnf(formula[1]))
            elif formula == 'and':
                return (to_cnf(formula[0]), to_cnf(formula[1]))
            elif formula == 'not':
                return (-to_cnf(formula[0]),)
        
        def dpll(clauses, assignment):
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_assignment = assignment.copy()
                new_assignment[literal] = literal > 0
                if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                    return True
                else:
                    new_assignment[literal] = not literal > 0
                    if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                        return True
            pure_literal = next((l for l in variables if all(l not in c or -l in c for c in clauses)), None)
            if pure_literal:
                new_assignment[pure_literal] = pure_literal > 0
                if dpll([c for c in clauses if pure_literal not in c and -pure_literal not in c], new_assignment):
                    return True
            literal = next((l for l in range(-n, n+1) if l not in assignment and -l not in assignment), None)
            if literal is None:
                return False
            new_assignment[literal] = literal > 0
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            else:
                new_assignment[literal] = not literal > 0
                return dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment)
        
        def cnf_to_clauses(cnf):
            clauses = []
            for clause in cnf:
                if isinstance(clause, int):
                    clauses.append((clause,))
                elif isinstance(clause, tuple):
                    clauses.append(clause)
            return clauses
        
        formula = generate_random_boolean_function(n)
        cnf = to_cnf(formula)
        clauses = cnf_to_clauses(cnf)
        
        return len(clauses) if dpll(clauses, {}) else float('inf')
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)) / n)
        return cov / (std_x * std_y) if std_x * std_y != 0 else float('nan')
    
    n_values = [5, 10, 15, 20, 30, 40]
    H_min_g_f = []
    s_f = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        tensor = tensor_representation(f, n)
        H_min_g_f.append(geometric_entropy(tensor, n))
        s_f.append(circuit_size(f, n))
    
    correlation = correlation_coefficient(H_min_g_f, [math.log(s) for s in s_f])
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.7,
        "counterexample": "" if correlation >= 0.7 else f"Correlation {correlation} < 0.7"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation < 0.7\" first_failing_seed={first_failing_seed}")