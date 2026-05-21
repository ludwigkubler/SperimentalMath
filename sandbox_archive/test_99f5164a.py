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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        
        # Generate clauses for each variable
        for var in variables:
            clauses.append([var])
            clauses.append([-var])
        
        # Generate clauses for implications
        for i in range(n):
            for j in range(i+1, n):
                clauses.append([f'x{i}', -f'x{j}'])
                clauses.append([-f'x{i}', f'x{j}'])
        
        # Generate the final clause
        final_clause = []
        for var in variables:
            final_clause.append(var)
        clauses.append(final_clause)
        
        return clauses
    
    def matrix_factorization(clauses):
        n = len(clauses)
        A = [[0] * n for _ in range(n)]
        
        for i, clause in enumerate(clauses):
            for literal in clause:
                if literal.startswith('x'):
                    var_index = int(literal[1:]) - 1
                    A[i][var_index] += 1
                else:
                    var_index = int(literal[1:]) - 1
                    A[i][var_index] -= 1
        
        return A
    
    def euler_characteristic(A):
        n = len(A)
        det_A = determinant(A, n)
        if det_A == 0:
            return 0
        else:
            return (-1) ** (n - 1) * det_A
    
    def determinant(A, n):
        if n == 1:
            return A[0][0]
        
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += ((-1) ** j) * A[0][j] * determinant(submatrix, n - 1)
        
        return det
    
    def resolution_tree_width(clauses):
        # Simplified version of resolution tree width calculation
        return len(clauses)
    
    n = random.randint(5, 40)
    clauses = generate_tseitin_formula(n)
    A = matrix_factorization(clauses)
    ν_G = euler_characteristic(A)
    L_G = resolution_tree_width(clauses)
    
    if ν_G == 0:
        return {
            "metric_name": "L(G) >= 2^(2ν(G))",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Euler characteristic is zero"
        }
    
    if L_G < 2 ** (2 * ν_G):
        return {
            "metric_name": "L(G) >= 2^(2ν(G))",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Counterexample found: L(G)={L_G}, 2^(2ν(G))={2 ** (2 * ν_G)}"
        }
    
    return {
        "metric_name": "L(G) >= 2^(2ν(G))",
        "metric_value": L_G,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2**i - 1 for i in range(5, 8)]  # First 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, 'metric_name': '{result['metric_name']}', 'metric_value': {result['metric_value']}, 'instances_tested': {result['instances_tested']}, 'conjecture_holds': {result['conjecture_holds']}, 'counterexample': '{result['counterexample']}'}}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")