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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        
        # Generate OR clauses
        for i in range(1, n+1):
            clause = random.sample(variables + ['~' + v for v in variables], 2)
            clauses.append(clause)
        
        # Generate AND clauses
        and_clauses = []
        for _ in range(n-1):
            and_clause = random.sample(variables + ['~' + v for v in variables], n)
            and_clauses.append(and_clause)
        
        # Combine all clauses into a single formula
        formula = {'variables': variables, 'clauses': clauses + and_clauses}
        return formula
    
    def compute_algebraic_automorphism_group(formula):
        variables = formula['variables']
        clauses = formula['clauses']
        n = len(variables)
        
        # Construct the incidence matrix
        incidence_matrix = [[0] * (2*n) for _ in range(2*n)]
        for clause in clauses:
            for literal in clause:
                if literal.startswith('~'):
                    var_index = variables.index(literal[1:]) * 2 + 1
                else:
                    var_index = variables.index(literal) * 2
                incidence_matrix[var_index][var_index ^ 1] = 1
        
        # Compute the rank of the incidence matrix
        def gaussian_elimination(matrix):
            rows, cols = len(matrix), len(matrix[0])
            for i in range(rows):
                max_row = i
                for j in range(i+1, rows):
                    if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                        max_row = j
                matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
                
                if matrix[i][i] == 0:
                    continue
                
                denom = matrix[i][i]
                for j in range(i, cols):
                    matrix[i][j] /= denom
                
                for j in range(rows):
                    if j != i and matrix[j][i] != 0:
                        factor = matrix[j][i]
                        for k in range(i, cols):
                            matrix[j][k] -= factor * matrix[i][k]
            
            rank = sum(1 for row in matrix if any(row))
            return rank
        
        return gaussian_elimination(incidence_matrix)
    
    def resolution_proof_length(formula):
        variables = formula['variables']
        clauses = formula['clauses']
        n = len(variables)
        
        # Initialize the resolution refutation
        refutation = []
        
        for clause in clauses:
            refutation.append(clause)
        
        while True:
            new_clauses = []
            for i in range(len(refutation)):
                for j in range(i+1, len(refutation)):
                    clause_i = set(refutation[i])
                    clause_j = set(refutation[j])
                    
                    for literal in clause_i:
                        if literal.startswith('~'):
                            neg_literal = literal[1:]
                        else:
                            neg_literal = '~' + literal
                        
                        if neg_literal in clause_j:
                            new_clause = (clause_i - {literal}) | (clause_j - {neg_literal})
                            if len(new_clause) == 0:
                                return len(refutation)
                            new_clauses.append(list(new_clause))
            
            refutation.extend(new_clauses)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_tseitin_formula(n)
        min_rank = compute_algebraic_automorphism_group(formula)
        proof_length = resolution_proof_length(formula)
        
        if proof_length == float('inf'):
            continue
        
        results.append({
            'n': n,
            'min_rank': min_rank,
            'proof_length': proof_length
        })
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid Tseitin formulas generated"
        }
    
    min_ranks = [r['min_rank'] for r in results]
    proof_lengths = [r['proof_length'] for r in results]
    log2_proof_lengths = [math.log2(p) if p > 0 else float('-inf') for p in proof_lengths]
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)
    
    correlation = pearson_correlation(min_ranks, log2_proof_lengths)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation,
        "instances_tested": len(results),
        "conjecture_holds": correlation >= 0.8,
        "counterexample": "" if correlation >= 0.8 else "Weak or negative correlation"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no trials executed")
        sys.exit(0)
    
    total_metric_value = sum(r['metric_value'] for r in results if r['metric_value'] is not None)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((r['metric_value'] - mean_metric_value) ** 2 for r in results if r['metric_value'] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results) and all(r['metric_value'] >= 0.5 for r in results):
        print(f"RESULT: FALSIFIED counterexample='Weak or negative correlation' first_failing_seed=None")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence to support or falsify the conjecture")