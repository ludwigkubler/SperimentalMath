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
    
    def generate_xor_3cnf(n):
        clauses = []
        for _ in range(2**n // 4):  # Generate a few clauses to ensure complexity
            literals = [random.choice([f'x{i}', f'~x{i}']) for i in range(1, n+1)]
            random.shuffle(literals)
            clause = ' ^ '.join(literals) + ' ^ (~'.join(literals[::-1]) + ')'
            clauses.append(clause)
        return ' v '.join(clauses)
    
    def parse_xor_3cnf(formula):
        literals = set()
        for clause in formula.split(' v '):
            for literal in clause.split(' ^ '):
                if literal.startswith('~'):
                    literals.add(literal[1:])
                else:
                    literals.add(literal)
        return literals
    
    def construct_quadratic_form(n, literals):
        q = [[0] * n for _ in range(n)]
        for literal in literals:
            if literal.startswith('~'):
                var = int(literal[1:]) - 1
                q[var][var] += 1
            else:
                var = int(literal) - 1
                q[var][var] -= 1
        return q
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find pivot row
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate below the pivot
            for j in range(i+1, n):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        
        # Back-substitute to find solution
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = matrix[i][-1] / matrix[i][i]
            for j in range(i-1, -1, -1):
                matrix[j][-1] -= matrix[j][i] * x[i]
        return x
    
    def minimal_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if all(abs(matrix[i][j]) < 1e-9 for j in range(n)):
                continue
            rank += 1
            for j in range(i+1, n):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    def monomial_circuit_size(formula):
        literals = parse_xor_3cnf(formula)
        circuit_size = len(literals)  # Simplistic estimate
        return circuit_size
    
    n = random.randint(5, 40)
    formula = generate_xor_3cnf(n)
    q_form = construct_quadratic_form(n, parse_xor_3cnf(formula))
    rank = minimal_rank(q_form)
    circuit_size = monomial_circuit_size(formula)
    
    if circuit_size == 0:
        return {
            "metric_name": "Ratio of Minimal Rank to Circuit Size",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Circuit size is zero"
        }
    
    ratio = rank / circuit_size
    return {
        "metric_name": "Ratio of Minimal Rank to Circuit Size",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True if ratio >= 0.5 else False,  # Placeholder for actual constant c
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 163))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Ratio too low' first_failing_seed={first_failing_seed}")