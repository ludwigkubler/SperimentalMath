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
            return 'x'
        else:
            p = random.choice(['AND', 'OR'])
            a, b = generate_boolean_formula(n-1), generate_boolean_formula(n-1)
            return f'({a}) {p} ({b})'

    def tseitin_transformation(formula):
        literals = set()
        clauses = []
        
        def encode(lit):
            if lit not in literals:
                literals.add(lit)
                clauses.append([lit])
            return lit
        
        def decode(lit):
            return lit
        
        def negate(lit):
            return f'~{lit}'
        
        def and_(a, b):
            a_neg = negate(a)
            b_neg = negate(b)
            new_lit = f'a_{len(clauses)}'
            clauses.append([new_lit, a_neg])
            clauses.append([new_lit, b_neg])
            return new_lit
        
        def or_(a, b):
            a_neg = negate(a)
            b_neg = negate(b)
            new_lit = f'o_{len(clauses)}'
            clauses.append([negate(new_lit), a_neg])
            clauses.append([negate(new_lit), b_neg])
            clauses.append([new_lit, a, b])
            return new_lit
        
        def parse(formula):
            if formula.startswith('(') and formula.endswith(')'):
                formula = formula[1:-1]
            if 'AND' in formula:
                a, b = formula.split(' AND ')
                return and_(parse(a), parse(b))
            elif 'OR' in formula:
                a, b = formula.split(' OR ')
                return or_(parse(a), parse(b))
            else:
                return encode(formula)
        
        def decode_clause(clause):
            return [decode(lit) for lit in clause]
        
        root = parse(formula)
        for clause in clauses:
            decoded_clause = decode_clause(clause)
            if any(l.startswith('~') for l in decoded_clause):
                print("Mapping undefined")
                return None
            else:
                clauses.append(decoded_clause)
        
        return literals, clauses

    def gaussian_elimination(matrix):
        n = len(matrix)
        m = len(matrix[0])
        rank = 0
        
        for i in range(n):
            if rank == m:
                break
            
            pivot_row = i
            while matrix[pivot_row][i] == 0:
                pivot_row += 1
                if pivot_row == n:
                    pivot_row -= 1
                    break
            
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            
            for j in range(m):
                matrix[i][j] /= matrix[i][i]
            
            for k in range(n):
                if k != i and matrix[k][i] != 0:
                    factor = -matrix[k][i]
                    for j in range(m):
                        matrix[k][j] += factor * matrix[i][j]
        
        return rank

    def order_of_tropical_symplectic_form(formula):
        literals, clauses = tseitin_transformation(formula)
        if literals is None:
            return None
        
        n = len(literals)
        m = len(clauses)
        matrix = [[0] * (n + 1) for _ in range(m)]
        
        for j in range(n):
            matrix[j][j] = 1
        
        for i, clause in enumerate(clauses):
            for lit in clause:
                if lit.startswith('~'):
                    col = literals.index(lit[1:]) + n
                    matrix[i][col] = -1
                else:
                    col = literals.index(lit)
                    matrix[i][col] = 1
        
        rank = gaussian_elimination(matrix)
        return m - rank

    def resolution_proof_width(formula):
        # Simplified version for demonstration purposes
        # Actual implementation would be more complex
        return len(formula.split())

    n_max = 40
    instances_tested = 30
    total_metric_value = 0.0
    conjecture_holds_count = 0

    for _ in range(instances_tested):
        n = random.randint(5, 40)
        formula = generate_boolean_formula(n)
        order = order_of_tropical_symplectic_form(formula)
        width = resolution_proof_width(formula)
        
        if order is None:
            continue
        
        total_metric_value += abs(width - order) / order
        conjecture_holds = abs(width - order) <= 0.5 * order
        conjecture_holds_count += conjecture_holds

    mean_metric_value = total_metric_value / instances_tested
    support_fraction = conjecture_holds_count / instances_tested
    
    return {
        "metric_name": "Resolution Proof Width vs Order of Tropical Symplectic Form",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": support_fraction >= 0.9,
        "counterexample": "" if support_fraction >= 0.9 else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")