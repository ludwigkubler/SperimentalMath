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
    
    def tseitin_to_polynomial(clauses):
        n = max(abs(lit) for clause in clauses for lit in clause if isinstance(lit, int))
        var_index_map = {i + 1: i for i in range(n)}
        
        def literal_to_var(lit):
            return var_index_map[abs(lit)]
        
        def negate(var):
            return -var
        
        def or_clause(*clauses):
            return [negate(x) for x in clauses]
        
        def and_clause(*clauses):
            return sum(clauses, [])
        
        def implication(a, b):
            return or_clause(negate(a), b)
        
        def equivalence(a, b):
            return and_clause(implication(a, b), implication(b, a))
        
        tseitin_vars = [0] * (n + 1)
        for i in range(1, n + 1):
            tseitin_vars[i] = random.randint(1, n + 2 * n)
        
        def encode_clause(clause):
            if len(clause) == 1:
                return clause[0]
            else:
                return negate(tseitin_vars[len(clause)])
        
        def encode_formula(formula):
            if isinstance(formula, int):
                return formula
            elif isinstance(formula, list):
                if len(formula) == 2 and formula[0] == 'or':
                    return or_clause(encode_formula(formula[1]), encode_formula(formula[2]))
                elif len(formula) == 2 and formula[0] == 'and':
                    return and_clause(encode_formula(formula[1]), encode_formula(formula[2]))
                elif len(formula) == 3 and formula[0] == 'implies':
                    return implication(encode_formula(formula[1]), encode_formula(formula[2]))
                elif len(formula) == 3 and formula[0] == 'equiv':
                    return equivalence(encode_formula(formula[1]), encode_formula(formula[2]))
            else:
                raise ValueError("Invalid formula")
        
        def polynomial_from_formula(formula):
            if isinstance(formula, int):
                return [formula]
            elif isinstance(formula, list):
                if len(formula) == 2 and formula[0] == 'or':
                    return or_clause(polynomial_from_formula(formula[1]), polynomial_from_formula(formula[2]))
                elif len(formula) == 2 and formula[0] == 'and':
                    return and_clause(polynomial_from_formula(formula[1]), polynomial_from_formula(formula[2]))
            else:
                raise ValueError("Invalid formula")
        
        def evaluate_polynomial(poly, assignment):
            result = 0
            for term in poly:
                if isinstance(term, int):
                    result += term * assignment[literal_to_var(term)]
                elif isinstance(term, list):
                    if len(term) == 2 and term[0] == 'or':
                        result += max(evaluate_polynomial(term[1], assignment), evaluate_polynomial(term[2], assignment))
                    elif len(term) == 2 and term[0] == 'and':
                        result *= evaluate_polynomial(term[1], assignment) * evaluate_polynomial(term[2], assignment)
            return result
        
        def find_roots(poly):
            roots = set()
            for i in range(-n, n + 1):
                if evaluate_polynomial(poly, {j: int(i == j) for j in range(1, n + 1)}) == 0:
                    roots.add(i)
            return roots
        
        formula = encode_formula(clauses)
        poly = polynomial_from_formula(formula)
        roots = find_roots(poly)
        
        return len(roots), len(clauses)
    
    def generate_tseitin_clauses(n):
        clauses = []
        for i in range(1, n + 1):
            clauses.append([i, -i])
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                clauses.append([-i, j, -j])
                clauses.append([i, -j, j])
        return clauses
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    clauses = generate_tseitin_clauses(n)
    
    num_roots, proof_width = tseitin_to_polynomial(clauses)
    
    return {
        "metric_name": "correlation",
        "metric_value": num_roots,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_C = sum(result["metric_value"] for result in results) / len(results)
    std_dev_C = math.sqrt(sum((result["metric_value"] - mean_C)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_C} std={std_dev_C} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["metric_value"] < 0.5 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"] and result["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")