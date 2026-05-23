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
    
    def tseitin_matrix(clauses):
        variables = set()
        new_vars = {}
        
        for clause in clauses:
            if len(clause) == 1:
                literals = clause
            else:
                literals = clause + [-x for x in clause]
            
            for literal in literals:
                if literal not in variables:
                    variables.add(literal)
            
            new_var = max(variables) + 1
            new_vars[clause] = new_var
            
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    matrix.append([new_var, -clause[i], -clause[j]])
        
        return matrix, variables
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        m = len(matrix[0])
        
        for i in range(n):
            # Find the pivot
            if matrix[i][i] == 0:
                for j in range(i + 1, n):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
                else:
                    return None  # Singular matrix
        
        # Eliminate above and below the pivot
        for i in range(n):
            for j in range(n):
                if i != j:
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(m):
                        matrix[j][k] -= factor * matrix[i][k]
        
        # Normalize the rows
        for i in range(n):
            pivot = matrix[i][i]
            for j in range(m):
                matrix[i][j] /= pivot
        
        return matrix
    
    def rank(matrix):
        if not matrix:
            return 0
        
        n = len(matrix)
        m = len(matrix[0])
        
        row_rank = 0
        col_rank = 0
        
        for i in range(n):
            if all(matrix[i][j] == 0 for j in range(m)):
                continue
            
            # Find a non-zero column to pivot on
            pivot_col = -1
            for j in range(m):
                if matrix[i][j] != 0:
                    pivot_col = j
                    break
            
            # Swap columns to bring the pivot to the first position
            if pivot_col != 0:
                matrix[i][:], matrix[i][pivot_col:] = matrix[i][pivot_col:], matrix[i][:pivot_col]
            
            # Normalize the row
            for j in range(m):
                matrix[i][j] /= matrix[i][0]
            
            # Eliminate above and below the pivot
            for j in range(n):
                if i != j:
                    factor = matrix[j][0]
                    for k in range(m):
                        matrix[j][k] -= factor * matrix[i][k]
            
            row_rank += 1
        
        return row_rank
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = [c for c in clauses if len(c) == 1]
        if unit_clause:
            literal = unit_clause[0][0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if -literal not in c], new_assignment):
                return True
            return False
        
        literal = random.choice(clauses[0])
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([c for c in clauses if literal not in c], new_assignment):
            return True
        new_assignment[literal] = False
        if dpll([c for c in clauses if -literal not in c], new_assignment):
            return True
        return False
    
    def height_dpll(clauses):
        assignment = {}
        return 1 + max(height_dpll(c) for c in clauses if literal in c)
    
    n = random.randint(5, 40)
    k = random.randint(2, min(n // 2, 10))
    clauses = []
    variables = set()
    
    for _ in range(random.randint(3 * n, 6 * n)):
        clause_size = random.randint(1, k)
        literals = [random.choice([-i, i]) for i in range(1, n + 1)]
        if len(set(literals)) == clause_size:
            clauses.append(literals)
    
    matrix, variables = tseitin_matrix(clauses)
    rank_value = rank(gaussian_elimination(matrix))
    height = height_dpll(clauses)
    
    expected_rank = math.log(n) / math.log(k)
    within_margin = abs(rank_value - expected_rank) <= 0.1 * expected_rank
    
    return {
        "metric_name": "rank",
        "metric_value": rank_value,
        "instances_tested": len(clauses),
        "conjecture_holds": within_margin and height == expected_rank,
        "counterexample": "" if within_margin else f"Rank {rank_value} vs. expected {expected_rank}, Height {height}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    total_rank = 0
    count_support = 0
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        total_rank += result["metric_value"]
        if result["conjecture_holds"]:
            count_support += 1
    
    mean_rank = total_rank / len(seeds)
    support_fraction = count_support / len(seeds)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0 support_fraction={support_fraction}")
    elif any(result["conjecture_holds"] is False for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")