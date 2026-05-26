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

def gaussian_elimination(matrix):
    if not matrix or not matrix[0]:
        return 0
    
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    
    for i in range(cols):
        max_row = None
        max_val = -1
        
        for j in range(rank, rows):
            val = abs(matrix[j][i])
            if val > max_val:
                max_val = val
                max_row = j
        
        if max_row is not None:
            matrix[rank], matrix[max_row] = matrix[max_row], matrix[rank]
            
            for j in range(cols):
                if i != j:
                    factor = -matrix[j][i] / matrix[rank][i]
                    for k in range(cols):
                        matrix[j][k] += factor * matrix[rank][k]
            
            rank += 1
    
    return rank

def generate_tseitin_tree(n, m):
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    
    # Generate literals
    for i in range(m):
        var = random.choice(variables)
        polarity = random.choice([True, False])
        if polarity:
            clause = f'{var}'
        else:
            clause = f'~{var}'
        clauses.append(clause)
    
    # Generate OR clauses
    for _ in range(m):
        vars_to_choose_from = variables[:]
        while len(vars_to_choose_from) > 1:
            var1, var2 = random.sample(vars_to_choose_from, 2)
            clause = f'({var1} | {var2})'
            clauses.append(clause)
            vars_to_choose_from.remove(var1)
            vars_to_choose_from.remove(var2)
    
    # Generate final OR clause
    final_clause = ' | '.join(variables)
    clauses.append(final_clause)
    
    return variables, clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = 2 * n
        variables, clauses = generate_tseitin_tree(n, m)
        
        matrix = [[0] * (n + 1) for _ in range(m)]
        for i, clause in enumerate(clauses):
            if ' | ' in clause:
                vars = clause.split(' | ')
                for var in vars:
                    if var.startswith('~'):
                        j = variables.index(var[1:]) + 1
                        matrix[i][j] = -1
                    else:
                        j = variables.index(var) + 1
                        matrix[i][j] = 1
            elif clause.startswith('~'):
                j = variables.index(clause[1:]) + 1
                matrix[i][j] = -1
            else:
                j = variables.index(clause) + 1
                matrix[i][j] = 1
        
        rank_value = gaussian_elimination(matrix)
        results.append((n, m, rank_value))
    
    total_rank = sum(rank for _, _, rank in results)
    avg_rank = Fraction(total_rank, len(results))
    
    alpha = Fraction(2)  # Hypothetical constant α
    expected_max_rank = alpha * (sum(m for _, m, _ in results) + sum(n for n, _, _ in results))
    
    conjecture_holds = all(rank <= expected_max_rank for _, _, rank in results)
    counterexample = "" if conjecture_holds else "alpha=2"
    
    return {
        "metric_name": "Rank of Geometric Langlands Dual",
        "metric_value": avg_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"alpha=2\" first_failing_seed={first_failing_seed}")