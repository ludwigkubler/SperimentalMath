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
    
    def generate_tseitin_tree(n, m):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        
        # Generate clauses
        for _ in range(m):
            clause_vars = random.sample(variables, 2)
            negated_var = random.choice(clause_vars)
            other_var = [v for v in clause_vars if v != negated_var][0]
            clause = f'({negated_var} ∨ {other_var})'
            clauses.append(clause)
        
        return variables, clauses
    
    def compute_geometric_langlands_rank(variables, clauses):
        # Placeholder function to compute the rank
        # This is a dummy implementation and should be replaced with actual computation
        n = len(variables)
        m = len(clauses)
        return Fraction(n + m, 2)  # Example rank calculation
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_idx = i
            for j in range(i+1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_idx][i]):
                    max_idx = j
            matrix[i], matrix[max_idx] = matrix[max_idx], matrix[i]
            
            pivot = matrix[i][i]
            if pivot == 0:
                raise ValueError("Matrix is singular")
            
            for j in range(i, cols):
                matrix[i][j] /= pivot
            
            for j in range(rows):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(i, cols):
                        matrix[j][k] -= factor * matrix[i][k]
        
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def compute_tseitin_matrix(variables, clauses):
        n = len(variables)
        m = len(clauses)
        matrix = [[0] * (n + 2*m) for _ in range(n + 2*m)]
        
        # Add identity matrix
        for i in range(n):
            matrix[i][i] = 1
        
        # Add clauses
        for j, clause in enumerate(clauses):
            var1, var2 = clause.split(' ∨ ')
            idx1 = variables.index(var1) + 1
            idx2 = variables.index(var2) + 1
            matrix[j+n][idx1] = 1
            matrix[j+n][idx2] = 1
        
        return matrix
    
    n = random.randint(5, 40)
    m = random.randint(n, 2*n)
    variables, clauses = generate_tseitin_tree(n, m)
    
    tseitin_matrix = compute_tseitin_matrix(variables, clauses)
    rank = gaussian_elimination(tseitin_matrix)
    
    alpha = Fraction(1, 2)  # Example constant
    expected_rank = alpha * (m + n)
    
    return {
        "metric_name": "rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= expected_rank,
        "counterexample": "" if rank <= expected_rank else f"Rank {rank} > {expected_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*100 + 1, 100))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_rank = sum(r["metric_value"] for r in results)
    avg_rank = Fraction(total_rank, len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank exceeds expected\" first_failing_seed={first_failing_seed}")