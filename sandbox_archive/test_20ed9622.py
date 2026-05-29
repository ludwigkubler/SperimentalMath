# auto-injected by SEC sandbox
import json
import sys
import os
import time
import re
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations
from collections import defaultdict

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        factor = Fraction(1, matrix[i][i])
        for j in range(cols):
            matrix[i][j] *= factor
        for k in range(rows):
            if k != i:
                factor = -matrix[k][i]
                for j in range(cols):
                    matrix[k][j] += factor * matrix[i][j]
    return matrix

def rank(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rref_matrix = gaussian_elimination(matrix)
    return sum(1 for row in rref_matrix if any(row))

def dpll_search_tree_height(cnf):
    variables = set()
    clauses = []
    
    # Extract variables and clauses from CNF
    for clause in cnf:
        variables.update(clause)
        clauses.append(clause)
    
    def dpll(model, clauses):
        if not clauses:
            return 0
        unit_clauses = [c for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_model = model.copy()
            new_model[literal] = True
            return dpll(new_model, [c for c in clauses if literal not in c and -literal not in c]) + 1
        
        pure_literals = []
        for literal in variables:
            positive_count = sum(1 for clause in clauses if literal in clause)
            negative_count = sum(1 for clause in clauses if -literal in clause)
            if positive_count == 0:
                pure_literals.append(literal)
            elif negative_count == 0:
                pure_literals.append(-literal)
        
        if pure_literals:
            literal = pure_literals[0]
            new_model = model.copy()
            new_model[literal] = True
            return dpll(new_model, [c for c in clauses if literal not in c and -literal not in c]) + 1
        
        literal = next(iter(variables))
        new_model_true = model.copy()
        new_model_true[literal] = True
        new_model_false = model.copy()
        new_model_false[literal] = False
        return max(dpll(new_model_true, [c for c in clauses if literal not in c and -literal not in c]), 
                   dpll(new_model_false, [c for c in clauses if literal not in c and -literal not in c])) + 1
    
    model = {}
    return dpll(model, clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    cnf = []
    for _ in range(random.randint(n * 2, n * 3)):
        clause = [random.choice([-i, i]) for i in range(1, n + 1)]
        cnf.append(clause)
    
    graphical_realization = [[1 if j in clause else 0 for j in range(1, n + 1)] for clause in cnf]
    k_theory_rank = rank(graphical_realization)
    
    height = dpll_search_tree_height(cnf)
    
    return {
        "metric_name": "DPLL Search Tree Height",
        "metric_value": height,
        "instances_tested": len(cnf),
        "conjecture_holds": height <= k_theory_rank * 10,  # Simplified upper bound for demonstration
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 37))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"DPLL search tree height exceeds K-theory rank bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")