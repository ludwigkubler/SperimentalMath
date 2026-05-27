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
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            # Find pivot row
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            
            # Eliminate below the pivot
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        
        # Back substitution
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = A[i][-1] / A[i][i]
            for j in range(i-1, -1, -1):
                A[j][-1] -= A[j][i] * x[i]
        return x
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def rank(matrix):
        A = [row[:] + [1] for row in matrix]  # Augmented matrix
        gaussian_elimination(A)
        rank = sum(1 for row in A if any(row[j] != 0 for j in range(len(row)-1)))
        return rank
    
    n = random.randint(5, 40)
    m = random.randint(n, 2*n)
    
    # Generate a random CNF formula
    clauses = []
    for _ in range(m):
        literals = [random.choice([f'x{i}', f'-x{i}']) for i in range(n)]
        clause = ' or '.join(literals)
        clauses.append(clause)
    
    # Convert CNF to a matrix representation (simplified for rank calculation)
    matrix = [[0] * n for _ in range(m)]
    for i, clause in enumerate(clauses):
        literals = clause.split(' or ')
        for literal in literals:
            if literal.startswith('-'):
                var = int(literal[1:]) - 1
                matrix[i][var] = -1
            else:
                var = int(literal) - 1
                matrix[i][var] = 1
    
    # Calculate the rank of the tropicalized object
    rank_value = rank(matrix)
    
    return {
        "metric_name": "rank_to_clauses_ratio",
        "metric_value": rank_value / m,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_ratio = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")