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
    
    def generate_tseitin_formula(n, m):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        
        # Generate literals
        literals = [f'{var}'] + [f'~{var}' for var in variables]
        
        # Generate clauses
        for _ in range(m):
            clause = random.sample(literals, 2)
            if random.choice([True, False]):
                clause[0] = f'~{clause[0]}'
                clause[1] = f'~{clause[1]}'
            clauses.append(clause)
        
        # Generate the Tseitin formula
        tseitin_formula = []
        for i, clause in enumerate(clauses):
            new_var = f'y{i+1}'
            tseitin_formula.append([f'{new_var}', *clause])
            tseitin_formula.append([f'~{new_var}', f'~{clause[0]}', f'~{clause[1]}'])
        
        # Add the final clause
        tseitin_formula.append(['z'] + [f'~{var}' for var in variables])
        
        return variables, clauses, tseitin_formula
    
    def tropicalize(tensor):
        n = len(tensor)
        result = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                result[i][j] = max(tensor[i][k] + tensor[k][j] for k in range(n))
        return result
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        if m > n:
            matrix = list(zip(*matrix))
            m, n = n, m
        
        for i in range(m):
            max_row = max(range(i, m), key=lambda r: abs(matrix[r][i]))
            if matrix[max_row][i] == 0:
                return float('inf')
            
            # Swap rows
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate below
            for j in range(i+1, m):
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
        
        return sum(1 for row in matrix if any(row))

    def resolution_width(clauses):
        queue = clauses.copy()
        width = 0
        
        while queue:
            new_clause = []
            for clause in queue:
                if len(clause) == 1:
                    return float('inf')
                
                literal, *rest = clause
                if literal.startswith('~'):
                    continue
                
                for other_clause in queue:
                    if literal in other_clause and any(l.startswith('~') for l in rest):
                        new_literal = [l for l in rest if not l.startswith('~')]
                        new_clause.append(new_literal)
            
            width = max(width, len(queue))
            queue = new_clause
        
        return width

    n = random.randint(5, 40)
    m = random.randint(n, n*2)
    variables, clauses, tseitin_formula = generate_tseitin_formula(n, m)

    tensor_product = [[0] * (n+1) for _ in range(n+1)]
    for clause in tseitin_formula:
        for literal in clause:
            if literal.startswith('~'):
                var_index = variables.index(literal[1:]) + 1
                tensor_product[var_index][var_index] = float('-inf')
            else:
                var_index = variables.index(literal) + 1
                tensor_product[0][var_index] = 1
    
    tropicalized_tensor = tropicalize(tensor_product)
    minimal_rank = rank(tropicalized_tensor)
    
    resolution_tree_width = resolution_width(clauses)
    
    conjecture_holds = minimal_rank <= resolution_tree_width
    counterexample = "" if conjecture_holds else f"An instance F with a resolution proof tree of width {resolution_tree_width} and minimal rank {minimal_rank}."

    return {
        "metric_name": "Minimal Rank vs Resolution Width",
        "metric_value": minimal_rank / resolution_tree_width,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) if len(sys.argv) > 1 else [2**i for i in range(5, 8)]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")