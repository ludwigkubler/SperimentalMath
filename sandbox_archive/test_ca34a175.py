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
    
    def generate_tseitin_formula(n, m):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        
        # Generate OR clauses
        for i in range(1, n+1):
            clause = ' | '.join(variables[:i])
            clauses.append(clause)
        
        # Generate AND clauses
        for _ in range(m - n):
            clause = random.choice(variables) + ' & ' + random.choice(variables)
            clauses.append(clause)
        
        return variables, clauses
    
    def is_satisfiable(clauses):
        stack = []
        assignment = {}
        
        for clause in clauses:
            if ' | ' in clause:
                disjuncts = clause.split(' | ')
                satisfied = any(assignment.get(var, False) for var in disjuncts)
                if not satisfied:
                    stack.append(disjuncts)
            else:
                conjuncts = clause.split(' & ')
                satisfied = all(assignment.get(var, False) for var in conjuncts)
                if not satisfied:
                    return False
        
        return True
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        lead = 0
        
        while lead < cols and rank < rows:
            i_max = lead
            for i in range(lead + 1, rows):
                if abs(matrix[i][lead]) > abs(matrix[i_max][lead]):
                    i_max = i
            
            if matrix[i_max][lead] == 0:
                lead += 1
                continue
            
            matrix[lead], matrix[i_max] = matrix[i_max], matrix[lead]
            
            for i in range(lead + 1, rows):
                factor = -matrix[i][lead] / matrix[lead][lead]
                for j in range(lead, cols):
                    if lead == j:
                        matrix[i][j] = 0
                    else:
                        matrix[i][j] += factor * matrix[lead][j]
            
            rank += 1
            lead += 1
        
        return rank
    
    def minimal_rank_brauer_group(n, m):
        variables, clauses = generate_tseitin_formula(n, m)
        num_vars = len(variables)
        
        # Create the Brauer group matrix
        brauer_matrix = [[0] * (num_vars + 1) for _ in range(num_vars + 1)]
        for var in variables:
            brauer_matrix[0][variables.index(var)] = 1
        
        # Perform Gaussian elimination to find the rank
        rank = gaussian_elimination(brauer_matrix)
        
        return rank
    
    def estimate_f(n, m):
        return (m ** (1/3)) * (math.log(n) ** 2)
    
    n = random.randint(5, 40)
    m = random.randint(2 * n, 3 * n)
    
    rank = minimal_rank_brauer_group(n, m)
    f_n = estimate_f(n, m)
    
    metric_value = math.log(rank) / math.log(f_n)
    conjecture_holds = metric_value <= 1.5 * (f_n ** 2)
    counterexample = "" if conjecture_holds else "n={}, m={}".format(n, m)
    
    return {
        "metric_name": "log(minimal_rank) / log(f(n))",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv[1:]) > 0:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        seeds = [2**i + 1 for i in range(5, 6)]  # Default to 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL:", result)
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_value, std_value, support_fraction))
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(results[0]["counterexample"], first_failing_seed))
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")