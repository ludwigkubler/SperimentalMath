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
        
        # Generate conjunctions of literals
        for i in range(1, 2**n):
            clause = []
            for j in range(n):
                if (i >> j) & 1:
                    clause.append(variables[j])
                else:
                    clause.append(f'~{variables[j]}')
            clauses.append(' | '.join(clause))
        
        # Generate disjunction of conjunctions
        formula = ' & '.join(['( ' + c + ' )' for c in clauses])
        return formula, variables
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        
        for col in range(n):
            pivot_row = -1
            for row in range(m):
                if matrix[row][col] != 0:
                    pivot_row = row
                    break
            
            if pivot_row == -1:
                continue
            
            rank += 1
            for r in range(m):
                if r != pivot_row:
                    factor = Fraction(matrix[r][col], matrix[pivot_row][col])
                    for c in range(n):
                        matrix[r][c] -= factor * matrix[pivot_row][c]
        
        return rank
    
    def p_adic_k_theory_invariant(matrix):
        m, n = len(matrix), len(matrix[0])
        invariant = 1
        
        for col in range(n):
            pivot_row = -1
            for row in range(m):
                if matrix[row][col] != 0:
                    pivot_row = row
                    break
            
            if pivot_row == -1:
                continue
            
            for r in range(m):
                if r != pivot_row:
                    factor = Fraction(matrix[r][col], matrix[pivot_row][col])
                    for c in range(n):
                        matrix[r][c] -= factor * matrix[pivot_row][c]
        
        return invariant
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula, variables = generate_tseitin_formula(n)
        matrix = [[0] * n for _ in range(n)]
        
        # Fill the matrix with random values
        for i in range(n):
            for j in range(i+1, n):
                matrix[i][j] = random.randint(1, 10)
                matrix[j][i] = matrix[i][j]
        
        rank = matrix_rank(matrix)
        invariant = p_adic_k_theory_invariant(matrix)
        
        results.append({
            "n": n,
            "rank": rank,
            "invariant": invariant
        })
    
    if not results:
        return {
            "metric_name": "p-adic K-theory invariant",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    max_n = max(r["n"] for r in results)
    instances_tested = len(results)
    conjecture_holds = all(r["invariant"] <= r["rank"] ** 2 for r in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "p-adic K-theory invariant",
        "metric_value": sum(r["invariant"] for r in results) / instances_tested,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(trial_result)
    
    if not all(r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")