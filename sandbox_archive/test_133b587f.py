# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(n):
        literals = [f'x{i}' for i in range(1, n + 1)]
        clauses = []
        for r in range(1, len(literals) + 1):
            for combo in combinations(literals, r):
                clause = ' or '.join(combo)
                if random.choice([True, False]):
                    clause = f'not ({clause})'
                clauses.append(clause)
        return ' and '.join(clauses)

    def dpll_search_tree_width(phi):
        literals = set()
        for literal in phi.split():
            if literal.startswith('x'):
                literals.add(literal)
        
        def is_satisfiable(formula, assignment):
            for literal in formula:
                if literal.startswith('not '):
                    value = not assignment[literal[4:]]
                else:
                    value = assignment[literal]
                if value == False:
                    return False
            return True
        
        def dpll(formula, assignment):
            literals = set()
            for literal in formula.split():
                if literal.startswith('x'):
                    literals.add(literal)
            
            unit_clauses = [literal for literal in literals if literal not in assignment and 'not ' + literal not in assignment]
            if unit_clauses:
                literal = random.choice(unit_clauses)
                assignment[literal] = True
                return dpll(formula, assignment)
            
            pure_literals = {}
            for literal in literals:
                positive_count = sum(1 for clause in formula.split(' and ') if literal in clause)
                negative_count = sum(1 for clause in formula.split(' and ') if 'not ' + literal in clause)
                if positive_count == 0:
                    pure_literals[literal] = False
                elif negative_count == 0:
                    pure_literals[literal] = True
            
            if pure_literals:
                literal, value = random.choice(list(pure_literals.items()))
                assignment[literal] = value
                return dpll(formula, assignment)
            
            if not is_satisfiable(formula, assignment):
                return False
            
            literals = list(literals - set(assignment.keys()))
            if not literals:
                return True
            
            literal = random.choice(literals)
            assignment[literal] = True
            if dpll(formula, assignment):
                return True
            del assignment[literal]
            
            assignment[literal] = False
            if dpll(formula, assignment):
                return True
            del assignment[literal]
        
        return len(assignment) if dpll(phi, {}) else 0

    def galois_representation_order(phi):
        literals = set()
        for literal in phi.split():
            if literal.startswith('x'):
                literals.add(literal)
        
        n = len(literals)
        A = [[0] * (2 ** n) for _ in range(2 ** n)]
        for i, j in product(range(2 ** n), repeat=2):
            for k in range(n):
                if (i & (1 << k)) and not (j & (1 << k)):
                    A[i][j] += 1
        
        def gaussian_elimination(matrix):
            rows, cols = len(matrix), len(matrix[0])
            rank = 0
            for i in range(cols):
                pivot_row = -1
                for j in range(rank, rows):
                    if matrix[j][i]:
                        pivot_row = j
                        break
                if pivot_row == -1:
                    continue
                
                matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
                rank += 1
                
                for j in range(rows):
                    if i != j and matrix[j][i]:
                        factor = Fraction(matrix[j][i], matrix[pivot_row][i])
                        for k in range(cols):
                            matrix[j][k] -= factor * matrix[pivot_row][k]
            
            return rank
        
        return gaussian_elimination(A)
    
    n_max = 0
    instances_tested = 0
    total_min_order = 0
    total_w_phi = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        phi = generate_formula(n)
        min_order = galois_representation_order(phi)
        w_phi = dpll_search_tree_width(phi)
        
        if min_order > 0:
            total_min_order += min_order
            total_w_phi += w_phi
            instances_tested += 1
        
        n_max = max(n_max, n)
    
    if instances_tested == 0:
        return {
            "metric_name": "min_order",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "no_instances"
        }
    
    mean_min_order = total_min_order / instances_tested
    mean_w_phi = total_w_phi / instances_tested
    
    correlation_coefficient = (instances_tested * sum(min_order * w_phi for min_order, w_phi in zip([mean_min_order] * instances_tested, [mean_w_phi] * instances_tested)) - instances_tested * mean_min_order * mean_w_phi) / \
                              math.sqrt((instances_tested * sum(min_order ** 2 for min_order in [mean_min_order] * instances_tested) - instances_tested * mean_min_order ** 2) *
                                        (instances_tested * sum(w_phi ** 2 for w_phi in [mean_w_phi] * instances_tested) - instances_tested * mean_w_phi ** 2))
    
    conjecture_holds = correlation_coefficient >= 0.7 and all(min_order <= 1 * w_phi for min_order, w_phi in zip([mean_min_order] * instances_tested, [mean_w_phi] * instances_tested))
    
    return {
        "metric_name": "min_order",
        "metric_value": mean_min_order,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"mean_min_order={mean_min_order}, mean_w_phi={mean_w_phi}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and any(res["instances_tested"] > 30 for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_min_order={results[seeds.index(first_failing_seed)]['metric_value']}, mean_w_phi={results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")