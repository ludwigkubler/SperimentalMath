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
    
    def tseitin_matrix(clauses):
        variables = set()
        new_vars = {}
        matrix = []
        
        for clause in clauses:
            if len(clause) == 1:
                var = clause[0]
                variables.add(var)
                matrix.append([var])
            else:
                new_var = f"x_{len(variables)}"
                variables.add(new_var)
                new_vars[clause] = new_var
                
                row = [new_var]
                for literal in clause:
                    if literal.startswith('~'):
                        var = literal[1:]
                        row.append(f"~{var}")
                    else:
                        var = literal
                        row.append(var)
                
                matrix.append(row)
        
        return matrix, variables
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        
        for col in range(cols):
            pivot_row = None
            for row in range(rank, rows):
                if matrix[row][col] != 0:
                    pivot_row = row
                    break
            
            if pivot_row is not None:
                matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
                
                for r in range(rows):
                    if r != rank and matrix[r][col] != 0:
                        factor = -matrix[r][col] / matrix[rank][col]
                        for c in range(cols):
                            matrix[r][c] += factor * matrix[rank][c]
                
                rank += 1
        
        return rank
    
    def dpll_search_tree_height(clauses, variables):
        def solve(model):
            if not clauses:
                return True
            clause = next(c for c in clauses if any(l in model or f"~{l}" not in model for l in c))
            literal = next(l for l in clause if l in model)
            if literal.startswith('~'):
                return solve({**model, f"~{literal[1:]}": False})
            else:
                return solve({**model, literal: True}) or solve({**model, literal: False})
        
        return len(variables) + sum(1 for _ in range(len(variables)) if not solve({}))

    n = random.randint(5, 40)
    k = random.randint(2, min(n // 2, 10))
    clauses = []
    
    for i in range(k):
        clause = [f"x_{j}" for j in random.sample(range(n), random.randint(1, k))]
        if random.choice([True, False]):
            clause.append(f"~x_{random.randint(0, n-1)}")
        clauses.append(clause)
    
    matrix, variables = tseitin_matrix(clauses)
    rank = gaussian_elimination(matrix)
    height = dpll_search_tree_height(clauses, variables)
    
    expected_rank = math.log(n) / math.log(k)
    expected_height = math.log(n) / math.log(k)
    
    conjecture_holds = abs(rank - expected_rank) <= 0.1 * expected_rank and abs(height - expected_height) <= 0.1 * expected_height
    counterexample = "" if conjecture_holds else "rank_diff=±10%, height_diff=±10%"
    
    return {
        "metric_name": "Rank vs DPLL Height",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank_diff=±10%, height_diff=±10%\" first_failing_seed={first_failing_seed}")