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
    
    def frobenius_schur_indicator(matrix):
        n = len(matrix)
        trace = sum(matrix[i][i] for i in range(n))
        det = determinant(matrix)
        return (trace * det) / (n * det**2)
    
    def determinant(matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        det = 0
        for j in range(len(matrix)):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += ((-1)**j) * matrix[0][j] * determinant(submatrix)
        return det
    
    def frege_proof_depth(formula):
        # Simplified DPLL solver to estimate proof depth
        stack = []
        clauses = formula.split(' or ')
        variables = set()
        for clause in clauses:
            literals = clause.split(' and ')
            for literal in literals:
                if literal.startswith('~'):
                    variables.add(literal[1:])
                else:
                    variables.add(literal)
        
        def dpll(clauses, assignment):
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                var = literal[1:] if literal.startswith('~') else literal
                value = False if literal.startswith('~') else True
                assignment[var] = value
                new_clauses = [c for c in clauses if not any(l in c for l in (literal, f'~{var}'))]
                return dpll(new_clauses, assignment)
            pure_literal = next((l for l in variables if all(l in c or f'~{l}' in c for c in clauses)), None)
            if pure_literal:
                var = pure_literal[1:] if pure_literal.startswith('~') else pure_literal
                value = False if pure_literal.startswith('~') else True
                assignment[var] = value
                new_clauses = [c for c in clauses if not any(l in c for l in (pure_literal, f'~{var}'))]
                return dpll(new_clauses, assignment)
            var = variables.pop()
            assignment[var] = False
            if dpll(clauses, assignment):
                return True
            assignment[var] = True
            if dpll(clauses, assignment):
                return True
            variables.add(var)
            return False
        
        assignment = {}
        proof_depth = 0
        while not dpll(clauses, assignment):
            proof_depth += 1
            for var in assignment:
                if assignment[var]:
                    clauses = [c for c in clauses if f'~{var}' not in c]
                else:
                    clauses = [c for c in clauses if var not in c]
        return proof_depth
    
    def generate_formula(n, m):
        variables = [f'x{i+1}' for i in range(n)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables + ['~' + v for v in variables], 3)
            clauses.append(' and '.join(clause))
        return ' or '.join(clauses)
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_frobenius_schur = 0.0
    total_proof_depth = 0.0
    
    for n in n_values:
        for _ in range(5):
            formula = generate_formula(n, n)
            matrix = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
            frobenius_schur = frobenius_schur_indicator(matrix)
            proof_depth = frege_proof_depth(formula)
            total_frobenius_schur += frobenius_schur
            total_proof_depth += proof_depth
            instances_tested += 1
    
    mean_frobenius_schur = total_frobenius_schur / instances_tested
    mean_proof_depth = total_proof_depth / instances_tested
    correlation_coefficient = (instances_tested * sum(frobenius_schur * proof_depth for frobenius_schur, proof_depth in zip(total_frobenius_schur, total_proof_depth)) - 
                               mean_frobenius_schur * total_proof_depth) / math.sqrt(instances_tested * sum((frobenius_schur - mean_frobenius_schur)**2 for frobenius_schur in total_frobenius_schur) * 
                                                                 (instances_tested * sum((proof_depth - mean_proof_depth)**2 for proof_depth in total_proof_depth)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.9,
        "counterexample": "" if correlation_coefficient >= 0.9 else "correlation_coefficient < 0.9"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.9\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")