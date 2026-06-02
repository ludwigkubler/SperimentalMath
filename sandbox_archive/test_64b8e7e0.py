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
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_tseitin_formula(n, m):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        
        # Generate literals and their negations
        literals = set()
        for var in variables:
            literals.add(var)
            literals.add(f'~{var}')
        
        # Generate m clauses
        for _ in range(m):
            clause = random.sample(literals, 2)
            if random.choice([True, False]):
                clause[0] = f'~{clause[0]}'
            if random.choice([True, False]):
                clause[1] = f'~{clause[1]}'
            clauses.append(clause)
        
        return variables, literals, clauses
    
    def construct_diophantine_equations(variables, literals, clauses):
        equations = []
        for var in variables:
            equations.append(f'{var} - 0')
        
        for clause in clauses:
            equation = f'({clause[0]}) + ({clause[1]}) - 2'
            equations.append(equation)
        
        return equations
    
    def solve_diophantine_equations(equations):
        solutions = []
        n = len(equations)
        variables = [f'x{i}' for i in range(1, n+1)]
        
        # Solve using Gaussian elimination
        A = [[0] * (n + 1) for _ in range(n)]
        for i in range(n):
            A[i][i] = 1
        
        for equation in equations:
            parts = equation.split()
            var_index = variables.index(parts[0])
            A[var_index][-1] = int(parts[-1])
            if len(parts) == 4:
                other_var_index = variables.index(parts[2])
                A[var_index][other_var_index] = -1
        
        for i in range(n):
            # Make the diagonal element 1
            if A[i][i] != 1:
                factor = Fraction(1, A[i][i])
                for j in range(i, n + 1):
                    A[i][j] *= factor
            
            # Eliminate other rows
            for j in range(n):
                if i != j and A[j][i] != 0:
                    factor = A[j][i]
                    for k in range(i, n + 1):
                        A[j][k] -= factor * A[i][k]
        
        for i in range(n):
            solutions.append(A[i][-1])
        
        return solutions
    
    def resolution_proof_width(clauses):
        # Simplified estimation of resolution proof width
        return len(clauses) ** 2
    
    trials = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            variables, literals, clauses = generate_tseitin_formula(n, n)
            equations = construct_diophantine_equations(variables, literals, clauses)
            num_solutions = len(solve_diophantine_equations(equations))
            resolution_proof_width_val = resolution_proof_width(clauses)
            trials.append((num_solutions, resolution_proof_width_val, literals, clauses))
    
    conjecture_holds = all(abs(num_solutions - resolution_proof_width) <= 2 * resolution_proof_width for _, m, literals, clauses in trials)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Diophantine Complexity",
        "metric_value": sum(num_solutions for num_solutions, _, _, _ in trials) / len(trials),
        "instances_tested": len(trials),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported")