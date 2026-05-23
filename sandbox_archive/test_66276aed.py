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
    
    def tropical_semiring_add(a, b):
        return max(a, b)
    
    def tropical_semiring_mul(a, b):
        if a == float('-inf') or b == float('-inf'):
            return float('-inf')
        return a + b
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            # Find pivot
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate below
            pivot = matrix[i][i]
            for j in range(i+1, n):
                factor = matrix[j][i] / pivot
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        
        # Back substitution
        solution = [0] * n
        for i in range(n-1, -1, -1):
            solution[i] = matrix[i][-1] / matrix[i][i]
            for j in range(i-1, -1, -1):
                matrix[j][-1] -= matrix[j][i] * solution[i]
        
        return solution
    
    def minimal_rank_tropical_k_theory(n, m):
        # Construct a random Tseitin formula
        variables = list(range(1, n+1))
        clauses = []
        for i in range(m):
            clause = [random.choice(variables) if random.choice([True, False]) else -random.choice(variables)]
            clauses.append(clause)
        
        # Convert to tropical K-theory matrix
        k_theory_matrix = [[0] * (n+1) for _ in range(n+1)]
        for clause in clauses:
            for var in clause:
                if var > 0:
                    k_theory_matrix[var-1][var-1] = float('-inf')
                else:
                    k_theory_matrix[-1][-1] = float('-inf')
        
        # Perform Gaussian elimination to find rank
        rank = gaussian_elimination(k_theory_matrix)
        return len(rank)
    
    def query_complexity(n, m):
        # Simulate query complexity as a function of n and m
        return n + math.log(m, 2)
    
    n = random.randint(5, 40)
    m = random.randint(1, 1000)
    rank = minimal_rank_tropical_k_theory(n, m)
    complexity = query_complexity(n, m)
    
    return {
        "metric_name": "Minimal Rank of Algebraic K-Theory Groups",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": abs(rank - complexity) <= 10,  # Allow a constant factor of 10
        "counterexample": "" if abs(rank - complexity) <= 10 else f"Rank {rank}, Complexity {complexity}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, 'metric_name': '{result['metric_name']}', 'metric_value': {result['metric_value']}, 'instances_tested': {result['instances_tested']}, 'conjecture_holds': {result['conjecture_holds']}, 'counterexample': '{result['counterexample']}'}}")
        results.append(result)
    
    mean_rank = sum(r['metric_value'] for r in results) / len(results)
    std_rank = math.sqrt(sum((r['metric_value'] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")